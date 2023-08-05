# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:51:05 2016

@author: Dominic O'Kane
"""

import numpy as np
from numba import njit, float64, int64
from math import exp, log

from ...finutils.FinDate import FinDate
from ...finutils.FinCalendar import FinCalendar, FinCalendarTypes
from ...finutils.FinCalendar import FinDayAdjustTypes, FinDateGenRuleTypes
from ...finutils.FinDayCount import FinDayCount, FinDayCountTypes
from ...finutils.FinFrequency import FinFrequency, FinFrequencyTypes
from ...finutils.FinGlobalVariables import gDaysInYear
from ...finutils.FinMath import ONE_MILLION
from ...market.curves.FinInterpolate import FinInterpMethods, uinterpolate
from ...market.curves.FinDiscountCurve import FinDiscountCurve

useFlatHazardRateIntegral = True
standardRecovery = 0.40

##########################################################################


@njit(
    float64[:](
        float64,
        float64,
        float64[:],
        float64[:],
        float64[:],
        float64[:],
        float64[:],
        float64[:],
        int64),
    fastmath=True,
    cache=True)
def riskyPV01_NUMBA(teff,
                    accrualFactorPCDToNow,
                    paymentTimes,
                    yearFracs,
                    npLiborTimes,
                    npLiborValues,
                    npSurvTimes,
                    npSurvValues,
                    pv01Method):
    ''' Fast calculation of the risky PV01 of a CDS using NUMBA.
    The output is a numpy array of the full and clean risky PV01.'''

    method = FinInterpMethods.FLAT_FORWARDS.value

    couponAccruedIndicator = 1

    # Method 0 : This is the market standard which assumes that the coupon
    # accrued is treated as though on average default occurs roughly midway
    # through a coupon period.

    tncd = paymentTimes[1]

    # The first coupon is a special case which needs to be handled carefully
    # taking into account what coupon has already accrued and what has not
    qeff = uinterpolate(teff, npSurvTimes, npSurvValues, method)
    q1 = uinterpolate(tncd, npSurvTimes, npSurvValues, method)
    z1 = uinterpolate(tncd, npLiborTimes, npLiborValues, method)

    # this is the part of the coupon accrued from the previous coupon date to now
    # accrualFactorPCDToNow = dayCount.yearFrac(pcd,teff)

    # reference credit survives to the premium payment date
    fullRPV01 = q1 * z1 * yearFracs[1]

    # coupon accrued from previous coupon to today paid in full at default
    # before coupon payment
    fullRPV01 = fullRPV01 + z1 * \
        (qeff - q1) * accrualFactorPCDToNow * couponAccruedIndicator

    # future accrued from now to coupon payment date assuming default roughly
    # midway
    fullRPV01 += 0.5 * z1 * \
        (qeff - q1) * (yearFracs[1] - accrualFactorPCDToNow) * couponAccruedIndicator

    for it in range(2, len(paymentTimes)):

        t2 = paymentTimes[it]

        q2 = uinterpolate(t2, npSurvTimes, npSurvValues, method)
        z2 = uinterpolate(t2, npLiborTimes, npLiborValues, method)

        accrualFactor = yearFracs[it]

        # full coupon is paid at the end of the current period if survives to
        # payment date
        fullRPV01 += q2 * z2 * accrualFactor

        ####################################################################

        if couponAccruedIndicator == 1:

            if useFlatHazardRateIntegral:
                # This needs to be updated to handle small h+r
                tau = accrualFactor
                h12 = -log(q2 / q1) / tau
                r12 = -log(z2 / z1) / tau
                alpha = h12 + r12
                expTerm = 1.0 - exp(-alpha * tau) - alpha * \
                    tau * exp(-alpha * tau)
                dfullRPV01 = q1 * z1 * h12 * \
                    expTerm / abs(alpha * alpha + 1e-20)
            else:
                dfullRPV01 = 0.50 * (q1 - q2) * z2 * accrualFactor

            fullRPV01 = fullRPV01 + dfullRPV01

        ####################################################################

        q1 = q2

    cleanRPV01 = fullRPV01 - accrualFactorPCDToNow

    return np.array([fullRPV01, cleanRPV01])

##########################################################################

@njit(float64(float64, float64, float64[:], float64[:], float64[:], float64[:],
              float64, int64, int64), fastmath=True, cache=True)
def protectionLegPV_NUMBA(teff,
                          tmat,
                          npLiborTimes,
                          npLiborValues,
                          npSurvTimes,
                          npSurvValues,
                          contractRecovery,
                          numStepsPerYear,
                          protMethod):
    ''' Fast calculation of the CDS protection leg PV using NUMBA to speed up
    the numerical integration over time. '''

    method = FinInterpMethods.FLAT_FORWARDS.value
    dt = (tmat - teff) / numStepsPerYear
    t = teff
    z1 = uinterpolate(t, npLiborTimes, npLiborValues, method)
    q1 = uinterpolate(t, npSurvTimes, npSurvValues, method)

    protPV = 0.0
    small = 1e-8

    if useFlatHazardRateIntegral is True:

        for i in range(0, numStepsPerYear):

            t = t + dt
            z2 = uinterpolate(t, npLiborTimes, npLiborValues, method)
            q2 = uinterpolate(t, npSurvTimes, npSurvValues, method)
            # This needs to be updated to handle small h+r
            h12 = -log(q2 / q1) / dt
            r12 = -log(z2 / z1) / dt
            expTerm = exp(-(r12 + h12) * dt)
            dprotPV = h12 * (1.0 - expTerm) * q1 * z1 / \
                (abs(h12 + r12) + small)
            protPV += dprotPV
            q1 = q2
            z1 = z2

    else:

        for i in range(0, numStepsPerYear):

            t += dt
            z2 = uinterpolate(t, npLiborTimes, npLiborValues, method)
            q2 = uinterpolate(t, npSurvTimes, npSurvValues, method)
            dq = q1 - q2
            dprotPV = 0.5 * (z1 + z2) * dq
            protPV += dprotPV
            q1 = q2
            z1 = z2

    protPV = protPV * (1.0 - contractRecovery)
    return protPV

##########################################################################
##########################################################################


class FinCDS(object):
    ''' A class which manages a Credit Default Swap. It performs schedule
    generation and the valuation and risk management of CDS. '''

    def __init__(self,
                 stepInDate, #  FinDate is when protection starts (usually T+1)
                 maturityDateOrTenor,  # FinDate or a FinTenor
                 runningCoupon, # Annualised coupon on premium leg
                 notional=ONE_MILLION,
                 longProtection=True,
                 frequencyType=FinFrequencyTypes.QUARTERLY,
                 dayCountType=FinDayCountTypes.ACT_360,
                 calendarType=FinCalendarTypes.WEEKEND,
                 busDayAdjustType=FinDayAdjustTypes.FOLLOWING,
                 dateGenRuleType=FinDateGenRuleTypes.BACKWARD):
        ''' Create a CDS from the step-in date, maturity date and coupon '''

        if type(stepInDate) is not FinDate:
            raise ValueError(
                "Step in date must be a FinDate")

        if type(maturityDateOrTenor) == FinDate:
            maturityDate = maturityDateOrTenor
        else:
            maturityDate = stepInDate.addTenor(maturityDateOrTenor)

        if type(runningCoupon) is not float and type(
                runningCoupon) is not np.float64:
            raise ValueError("Coupon is not float but is " +
                             str(type(runningCoupon)))

        if stepInDate > maturityDate:
            raise ValueError("Step in date after maturity date")

        if dayCountType not in FinDayCountTypes:
            raise ValueError(
                "Unknown Fixed Day Count Rule type " +
                str(dayCountType))

        if frequencyType not in FinFrequencyTypes:
            raise ValueError(
                "Unknown Fixed Frequency type " +
                str(frequencyType))

        if calendarType not in FinCalendarTypes:
            raise ValueError("Unknown Calendar type " + str(calendarType))

        if busDayAdjustType not in FinDayAdjustTypes:
            raise ValueError(
                "Unknown Business Day Adjust type " +
                str(busDayAdjustType))

        if dateGenRuleType not in FinDateGenRuleTypes:
            raise ValueError(
                "Unknown Date Gen Rule type " +
                str(dateGenRuleType))

        self._stepInDate = stepInDate
        self._maturityDate = maturityDate
        self._coupon = runningCoupon
        self._notional = notional
        self._longProtection = longProtection
        self._dayCountType = dayCountType
        self._dateGenRuleType = dateGenRuleType
        self._calendarType = calendarType
        self._frequencyType = frequencyType
        self._busDayAdjustType = busDayAdjustType

        self.generateAdjustedCDSPaymentDates()
        self.calcFlows()

##########################################################################

    def generateAdjustedCDSPaymentDates(self):
        ''' Generate CDS payment dates which have been holiday adjusted.'''
        frequency = FinFrequency(self._frequencyType)
        calendar = FinCalendar(self._calendarType)
        startDate = self._stepInDate
        endDate = self._maturityDate

        self._adjustedDates = []
        numMonths = int(12.0 / frequency)

        unadjustedScheduleDates = []

        if self._dateGenRuleType == FinDateGenRuleTypes.BACKWARD:

            nextDate = endDate
            flowNum = 0

            while nextDate > startDate:
                unadjustedScheduleDates.append(nextDate)
                nextDate = nextDate.addMonths(-numMonths)
                flowNum += 1

            # Add on the Previous Coupon Date
            unadjustedScheduleDates.append(nextDate)
            flowNum += 1

            # reverse order
            for i in range(0, flowNum):
                dt = unadjustedScheduleDates[flowNum - i - 1]
                self._adjustedDates.append(dt)

            # holiday adjust dates except last one
            for i in range(0, flowNum - 1):

                dt = calendar.adjust(self._adjustedDates[i],
                                     self._busDayAdjustType)

                self._adjustedDates[i] = dt

            finalDate = self._adjustedDates[flowNum - 1]

            # Final date is moved forward by one day
            self._adjustedDates[flowNum - 1] = finalDate.addDays(1)

        elif self._dateGenRuleType == FinDateGenRuleTypes.FORWARD:

            nextDate = startDate
            flowNum = 0

            unadjustedScheduleDates.append(nextDate)
            flowNum = 1

            while nextDate < endDate:
                unadjustedScheduleDates.append(nextDate)
                nextDate = nextDate.addMonths(numMonths)
                flowNum = flowNum + 1

            for i in range(1, flowNum):

                dt = calendar.adjust(unadjustedScheduleDates[i],
                                     self._busDayAdjustType)

                self._adjustedDates.append(dt)

            finalDate = endDate.addDays(1)
            self._adjustedDates.append(finalDate)

        else:
            raise ValueError("Unknown FinDateGenRuleType:" +
                             str(self._dateGenRuleType))

##########################################################################

    def calcFlows(self):
        ''' Calculate cash flow amounts on premium leg. '''
        paymentDates = self._adjustedDates
        dayCount = FinDayCount(self._dayCountType)

        self._accrualFactors = []
        self._flows = []

        self._accrualFactors.append(0.0)
        self._flows.append(0.0)

        numFlows = len(paymentDates)

        for it in range(1, numFlows):
            t0 = paymentDates[it - 1]
            t1 = paymentDates[it]
            accrualFactor = dayCount.yearFrac(t0, t1)
            flow = accrualFactor * self._coupon * self._notional

            self._accrualFactors.append(accrualFactor)
            self._flows.append(flow)

##########################################################################

    def value(self,
              valuationDate,
              issuerCurve,
              contractRecovery=standardRecovery,
              pv01Method=0,
              prot_method=0,
              numStepsPerYear=25):
        ''' Valuation of a CDS contract on a specific valuation date given
        an issuer curve and a contract recovery rate.'''

        rpv01 = self.riskyPV01(valuationDate,
                               issuerCurve,
                               pv01Method)

        fullRPV01 = rpv01['full_rpv01']
        cleanRPV01 = rpv01['clean_rpv01']

        protPV = self.protectionLegPV(valuationDate,
                                      issuerCurve,
                                      contractRecovery,
                                      numStepsPerYear,
                                      prot_method)

        fwdDf = 1.0

        if self._longProtection:
            longProt = +1
        else:
            longProt = -1

        fullPV = fwdDf * longProt * \
            (protPV - self._coupon * fullRPV01 * self._notional)
        cleanPV = fwdDf * longProt * \
            (protPV - self._coupon * cleanRPV01 * self._notional)

        return {'full_pv': fullPV, 'clean_pv': cleanPV}

##########################################################################

    def creditDV01(self,
                   valuationDate,
                   issuerCurve,
                   contractRecovery=standardRecovery,
                   pv01Method=0,
                   prot_method=0,
                   numStepsPerYear=25):
        ''' Calculation of the change in the value of the CDS contract for a
        one basis point change in the level of the CDS curve.'''

        v0 = self.value(valuationDate,
                        issuerCurve,
                        contractRecovery,
                        pv01Method,
                        prot_method,
                        numStepsPerYear)

        survProbs = issuerCurve._values

        bump = 0.0001
        for cds in issuerCurve._cdsContracts:
            cds._coupon += bump
        issuerCurve.buildCurve()

        v1 = self.value(valuationDate,
                        issuerCurve,
                        contractRecovery,
                        pv01Method,
                        prot_method,
                        numStepsPerYear)

        # NEED TO UNDO CHANGES TO CURVE OBJECT - NO NEED TO REBUILD !!!
        for cds in issuerCurve._cdsContracts:
            cds._coupon -= bump
        issuerCurve._values = survProbs

        creditDV01 = (v1['full_pv'] - v0['full_pv'])
        return creditDV01

##########################################################################

    def interestDV01(self,
                     valuationDate,
                     issuerCurve,
                     contractRecovery=standardRecovery,
                     pv01Method=0,
                     prot_method=0,
                     numStepsPerYear=25):
        ''' Calculation of the interest DV01 based on a simple bump of
        the discount factors and reconstruction of the CDS curve. '''

        v0 = self.value(valuationDate,
                        issuerCurve,
                        contractRecovery,
                        pv01Method,
                        prot_method,
                        numStepsPerYear)

        dfs = issuerCurve._liborCurve._values
        survProbs = issuerCurve._values

        bump = 0.0001
        for depo in issuerCurve._liborCurve._usedDeposits:
            depo._depositRate += bump
        for fra in issuerCurve._liborCurve._usedFRAs:
            fra._fraRate += bump
        for swap in issuerCurve._liborCurve._usedSwaps:
            swap._fixedCoupon += bump
        issuerCurve._liborCurve.buildCurve()
        issuerCurve.buildCurve()

        v1 = self.value(valuationDate,
                        issuerCurve,
                        contractRecovery,
                        pv01Method,
                        prot_method,
                        numStepsPerYear)

        # Need do undo changes to Libor curve object in issuer curve
        # Do not need to rebuild it - just restore initial dfs and surv probs.
        for depo in issuerCurve._liborCurve._usedDeposits:
            depo._depositRate -= bump
        for fra in issuerCurve._liborCurve._usedFRAs:
            fra._fraRate -= bump
        for swap in issuerCurve._liborCurve._usedSwaps:
            swap._fixedCoupon -= bump

        issuerCurve._liborCurve._values = dfs
        issuerCurve._values = survProbs

        creditDV01 = (v1[0] - v0[0])
        return creditDV01

##########################################################################

    def cashSettlementAmount(self,
                             valuationDate,
                             settlementDate,
                             issuerCurve,
                             contractRecovery=standardRecovery,
                             pv01Method=0,
                             prot_method=0,
                             numStepsPerYear=25):
        ''' Value of the contract on the settlement date including accrued
        interest. '''

        v = self.value(valuationDate,
                       issuerCurve,
                       contractRecovery,
                       pv01Method,
                       prot_method,
                       numStepsPerYear)

        liborCurve = issuerCurve._liborCurve
        df = liborCurve.df(settlementDate)
        v = v / df
        return v

##########################################################################

    def cleanPrice(self,
                   valuationDate,
                   issuerCurve,
                   contractRecovery=standardRecovery,
                   pv01Method=0,
                   prot_method=0,
                   numStepsPerYear=52):
        ''' Value of the CDS contract excluding accrued interest. '''

        riskyPV01 = self.riskyPV01(valuationDate, issuerCurve, pv01Method)

        cleanRPV01 = riskyPV01['clean_rpv01']

        protPV = self.protectionLegPV(valuationDate,
                                      issuerCurve,
                                      contractRecovery,
                                      numStepsPerYear,
                                      prot_method)

        fwdDf = 1.0

        cleanPV = fwdDf * (protPV - self._coupon * cleanRPV01 * self._notional)
        cleanPrice = (self._notional - cleanPV) / self._notional * 100.0
        return cleanPrice

##########################################################################

    def riskyPV01_OLD(self,
                      valuationDate,
                      issuerCurve,
                      pv01Method=0):
        ''' RiskyPV01 of the contract using the OLD method. '''

        paymentDates = self._adjustedDates
        dayCount = FinDayCount(self._dayCountType)

        couponAccruedIndicator = 1

        # Method 0 : This is the market standard which assumes that the coupon
        # accrued is treated as though on average default occurs roughly midway
        # through a coupon period.

        teff = self._stepInDate
        pcd = paymentDates[0]  # PCD
        ncd = paymentDates[1]  # NCD

        # The first coupon is a special case which must be handled carefully
        # taking into account what coupon has already accrued and what has not
        qeff = issuerCurve.survivalProbability(teff)
        q1 = issuerCurve.survivalProbability(ncd)
        z1 = issuerCurve.df(ncd)

        # this is the part of the coupon accrued from the previous coupon date
        # to now
        accrualFactorPCDToNow = dayCount.yearFrac(pcd, teff)

        # full first coupon is paid at the end of the current period if the
        yearFrac = dayCount.yearFrac(pcd, ncd)

        # reference credit survives to the premium payment date
        fullRPV01 = q1 * z1 * yearFrac

        # coupon accrued from previous coupon to today paid in full at default
        # before coupon payment
        fullRPV01 = fullRPV01 + z1 * \
            (qeff - q1) * accrualFactorPCDToNow * couponAccruedIndicator

        # future accrued from now to coupon payment date assuming default
        # roughly midway
        fullRPV01 = fullRPV01 + 0.5 * z1 * \
            (qeff - q1) * (yearFrac - accrualFactorPCDToNow) * couponAccruedIndicator

        for it in range(2, len(paymentDates)):

            t1 = paymentDates[it - 1]
            t2 = paymentDates[it]
            q2 = issuerCurve.survivalProbability(t2)
            z2 = issuerCurve.df(t2)

            accrualFactor = dayCount.yearFrac(t1, t2)

            # full coupon is paid at the end of the current period if survives
            # to payment date
            fullRPV01 += q2 * z2 * accrualFactor

            ###################################################################

            if couponAccruedIndicator == 1:

                if useFlatHazardRateIntegral:
                    # This needs to be updated to handle small h+r
                    tau = accrualFactor
                    h12 = -log(q2 / q1) / tau
                    r12 = -log(z2 / z1) / tau
                    alpha = h12 + r12
                    expTerm = 1.0 - exp(-alpha * tau) - \
                        alpha * tau * exp(-alpha * tau)
                    dfullRPV01 = q1 * z1 * h12 * \
                        expTerm / abs(alpha * alpha + 1e-20)
                else:
                    dfullRPV01 = 0.50 * (q1 - q2) * z2 * accrualFactor

                fullRPV01 = fullRPV01 + dfullRPV01

            ###################################################################

            q1 = q2

        cleanRPV01 = fullRPV01 - accrualFactorPCDToNow

#        print("OLD PV01",fullRPV01, cleanRPV01)

        return {'full_rpv01': fullRPV01, 'clean_rpv01': cleanRPV01}

##########################################################################

    def accruedDays(self):
        ''' Number of days between the previous coupon and the currrent step
        in date. '''

        # I assume accrued runs to the effective date
        paymentDates = self._adjustedDates
        pcd = paymentDates[0]
        accruedDays = (self._stepInDate - pcd)
        return accruedDays

##########################################################################

    def accruedInterest(self):
        ''' Calculate the amount of accrued interest that has accrued from the
        previous coupon date (PCD) to the stepInDate of the CDS contract. '''

        dayCount = FinDayCount(self._dayCountType)
        paymentDates = self._adjustedDates
        pcd = paymentDates[0]
        accrualFactor = dayCount.yearFrac(pcd, self._stepInDate)
        accruedInterest = accrualFactor * self._notional * self._coupon

        if self._longProtection:
            accruedInterest *= -1.0

        return accruedInterest

##########################################################################

    def protectionLegPV(self,
                        valuationDate,
                        issuerCurve,
                        contractRecovery=standardRecovery,
                        numStepsPerYear=25,
                        protMethod=0):
        ''' Calculates the protection leg PV of the CDS by calling into the
        fast NUMBA code that has been defined above. '''

        teff = (self._stepInDate - valuationDate) / gDaysInYear
        tmat = (self._maturityDate - valuationDate) / gDaysInYear

        liborCurve = issuerCurve._liborCurve

        v = protectionLegPV_NUMBA(teff,
                                  tmat,
                                  liborCurve._times,
                                  liborCurve._values,
                                  issuerCurve._times,
                                  issuerCurve._values,
                                  contractRecovery,
                                  numStepsPerYear,
                                  protMethod)

        return v * self._notional

##########################################################################

    def riskyPV01(self,
                  valuationDate,
                  issuerCurve,
                  pv01Method=0):
        ''' The riskyPV01 is the present value of a risky one dollar paid on
        the premium leg of a CDS contract. '''

        liborCurve = issuerCurve._liborCurve

        paymentTimes = []
        for it in range(0, len(self._adjustedDates)):
            t = (self._adjustedDates[it] - valuationDate) / gDaysInYear
            paymentTimes.append(t)

        # this is the part of the coupon accrued from the previous coupon date
        # to now
        pcd = self._adjustedDates[0]
        eff = self._stepInDate
        dayCount = FinDayCount(self._dayCountType)

        accrualFactorPCDToNow = dayCount.yearFrac(pcd, eff)

        yearFracs = self._accrualFactors
        teff = (eff - valuationDate) / gDaysInYear

        valueRPV01 = riskyPV01_NUMBA(teff,
                                     accrualFactorPCDToNow,
                                     np.array(paymentTimes),
                                     np.array(yearFracs),
                                     liborCurve._times,
                                     liborCurve._values,
                                     issuerCurve._times,
                                     issuerCurve._values,
                                     pv01Method)

        fullRPV01 = valueRPV01[0]
        cleanRPV01 = valueRPV01[1]

#        print("NEW PV01",fullRPV01, cleanRPV01)
        return {'full_rpv01': fullRPV01, 'clean_rpv01': cleanRPV01}

##########################################################################

    def premiumLegPV(self,
                     valuationDate,
                     issuerCurve,
                     pv01Method=0):
        ''' Value of the premium leg of a CDS. '''

        fullRPV01 = self.riskyPV01(valuationDate,
                                   issuerCurve,
                                   pv01Method)['full_rpv01']

        v = fullRPV01 * self._notional * self._coupon
        return v

##########################################################################

    def parSpread(self,
                  valuationDate,
                  issuerCurve,
                  contractRecovery=standardRecovery,
                  numStepsPerYear=25,
                  pv01Method=0,
                  protMethod=0):
        ''' Breakeven CDS coupon that would make the value of the CDS contract
        equal to zero. '''

        cleanRPV01 = self.riskyPV01(valuationDate,
                                    issuerCurve,
                                    pv01Method)['clean_rpv01']

        prot = self.protectionLegPV(valuationDate,
                                    issuerCurve,
                                    contractRecovery,
                                    numStepsPerYear,
                                    protMethod)

        # By convention this is calculated using the clean RPV01
        spd = prot / cleanRPV01 / self._notional
        return spd

##########################################################################

    def valueFastApprox(self,
                        valuationDate,
                        flatContinuousInterestRate,
                        flatCDSCurveSpread,
                        curveRecovery=standardRecovery,
                        contractRecovery=standardRecovery):
        ''' Implementation of fast valuation of the CDS contract using an
        accurate approximation that avoids curve building. '''

        if type(valuationDate) is not FinDate:
            raise ValueError(
                "Valuation date must be a FinDate and not " +
                str(valuationDate))

        t_mat = (self._maturityDate - valuationDate) / gDaysInYear
        t_eff = (self._stepInDate - valuationDate) / gDaysInYear

        h = flatCDSCurveSpread / (1.0 - curveRecovery)
        r = flatContinuousInterestRate
        fwdDf = 1.0

        if self._longProtection:
            longProtection = +1
        else:
            longProtection = -1

        accrued = self.accruedInterest()

        # This is the clean RPV01 as it treats the PV01 stream as though it
        # pays just the accrued for the time between 0 and the maturity
        # It therefore omits the part that has accrued
        cleanRPV01 = (exp(-(r + h) * t_eff) - exp(-(r + h)
                                                  * t_mat)) / (h + r) * 365.0 / 360.0
        protPV = h * (1.0 - contractRecovery) * (exp(-(r + h) * \
                      t_eff) - exp(-(r + h) * t_mat)) / (r + h) * self._notional
        cleanPV = fwdDf * longProtection * \
            (protPV - self._coupon * cleanRPV01 * self._notional)
        fullPV = cleanPV + fwdDf * longProtection * accrued

        bumpSize = 0.0001

        h = (flatCDSCurveSpread + bumpSize) / (1.0 - contractRecovery)
        r = flatContinuousInterestRate
        cleanRPV01 = (exp(-(r + h) * t_eff) - exp(-(r + h)
                                                  * t_mat)) / (h + r) * 365.0 / 360.0
        protPV = h * (1.0 - contractRecovery) * (exp(-(r + h) * \
                      t_eff) - exp(-(r + h) * t_mat)) / (r + h) * self._notional
        cleanPV_credit_bumped = fwdDf * longProtection * \
            (protPV - self._coupon * cleanRPV01 * self._notional)
        fullPV_credit_bumped = cleanPV_credit_bumped + fwdDf * longProtection * accrued
        credit01 = fullPV_credit_bumped - fullPV

        h = flatCDSCurveSpread / (1.0 - contractRecovery)
        r = flatContinuousInterestRate + bumpSize
        cleanRPV01 = (exp(-(r + h) * t_eff) - exp(-(r + h)
                                                  * t_mat)) / (h + r) * 365.0 / 360.0
        protPV = h * (1.0 - contractRecovery) * (exp(-(r + h) * \
                      t_eff) - exp(-(r + h) * t_mat)) / (r + h) * self._notional
        cleanPV_ir_bumped = fwdDf * longProtection * \
            (protPV - self._coupon * cleanRPV01 * self._notional)
        fullPV_ir_bumped = cleanPV_ir_bumped + fwdDf * longProtection * accrued
        ir01 = fullPV_ir_bumped - fullPV

        return (fullPV, cleanPV, credit01, ir01)

##########################################################################

    def print(self, valuationDate):
        ''' print out details of the CDS contract and all of the calculated
        cashflows '''
        print("STEPINDATE: ", str(self._stepInDate))
        print("MATURITY: ", str(self._maturityDate))
        print("NOTIONAL:", str(self._notional))
        print("RUNNING COUPON: ", str(self._coupon * 10000), "bp")
        print("DAYCOUNT: ", str(self._dayCountType))
        print("FREQUENCY: ", str(self._frequencyType))
        print("CALENDAR: ", str(self._calendarType))
        print("BUSDAYRULE: ", str(self._busDayAdjustType))
        print("DATEGENRULE: ", str(self._dateGenRuleType))

        accruedDays = self.accruedDays()
        print("ACCRUED DAYS:", str(accruedDays))

        numFlows = len(self._adjustedDates)

        print("PAYMENT_DATE      YEAR_FRAC      FLOW")

        for it in range(1, numFlows):
            dt = self._adjustedDates[it]
            accFactor = self._accrualFactors[it]
            flow = self._flows[it]
            print("%15s %10.6f %12.2f" % (dt, accFactor, flow))

##########################################################################

    def printFlows(self, issuerCurve):

        numFlows = len(self._adjustedDates)

        print("PAYMENT_DATE      YEAR_FRAC      FLOW           DF       SURV_PROB      NPV")

        for it in range(1, numFlows):
            dt = self._adjustedDates[it]
            accFactor = self._accrualFactors[it]
            flow = self._flows[it]
            z = issuerCurve.df(dt)
            q = issuerCurve.survProb(dt)
            print("%15s %10.6f %12.2f %12.6f %12.6f %12.2f" %
                  (dt, accFactor, flow, z, q, flow * z * q))

##########################################################################
