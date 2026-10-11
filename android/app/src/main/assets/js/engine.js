/**
 * InstaHealth: Zero-Cloud On-Device Health & Strain Calibration Engine
 * 
 * Rules:
 * - 100% on-device execution (no external network/cloud storage).
 * - Predefined age-stratified population baseline dataset.
 * - Continuous personal model adaptation (online weight updates per user).
 * - Multi-metric calculation: Strain (0-21), Active Calories, Exertion Delta, Recovery Needs.
 */

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.InstaHealthEngine = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Default embedded population baselines (fallback if data/baselines.json is offline)
  const DEFAULT_BASELINES = {
    age_cohorts: [
      { min_age: 18, max_age: 29, avg_resting_hr: 64, tanaka_max_hr: 195, baseline_active_burn_rate_cal_hr: 360, exertion_coefficient: 1.0, strain_thresholds: { light: 6.0, moderate: 12.0, strenuous: 16.0, peak: 21.0 } },
      { min_age: 30, max_age: 39, avg_resting_hr: 67, tanaka_max_hr: 185, baseline_active_burn_rate_cal_hr: 330, exertion_coefficient: 1.05, strain_thresholds: { light: 5.8, moderate: 11.5, strenuous: 15.5, peak: 20.5 } },
      { min_age: 40, max_age: 49, avg_resting_hr: 70, tanaka_max_hr: 176, baseline_active_burn_rate_cal_hr: 300, exertion_coefficient: 1.12, strain_thresholds: { light: 5.5, moderate: 11.0, strenuous: 15.0, peak: 20.0 } },
      { min_age: 50, max_age: 59, avg_resting_hr: 72, tanaka_max_hr: 168, baseline_active_burn_rate_cal_hr: 270, exertion_coefficient: 1.20, strain_thresholds: { light: 5.2, moderate: 10.5, strenuous: 14.2, peak: 19.5 } },
      { min_age: 60, max_age: 99, avg_resting_hr: 74, tanaka_max_hr: 158, baseline_active_burn_rate_cal_hr: 240, exertion_coefficient: 1.30, strain_thresholds: { light: 4.8, moderate: 9.8, strenuous: 13.5, peak: 19.0 } }
    ]
  };

  const STORAGE_KEY_PROFILES = 'instahealth_profiles_v2';
  const STORAGE_KEY_ACTIVE_ID = 'instahealth_active_profile_id_v2';

  const DEFAULT_PROFILES = [
    {
      id: 'p_runner',
      emoji: '🏃‍♂️',
      name: 'Runner',
      sex: 'male',
      age: 24,
      restingHR: 58,
      currentDay: 3, // Calibrated
      historyDays: [
        { day: 1, steps: 11400, activeCalories: 520, avgHR: 138, restingHR: 57, sleepHours: 8.2, strain: 12.4 },
        { day: 2, steps: 12100, activeCalories: 560, avgHR: 142, restingHR: 58, sleepHours: 8.0, strain: 13.1 }
      ],
      model: { hrWeight: 0.55, calWeight: 0.35, cadenceWeight: 0.10, adaptationEpochs: 2, personalEfficiencyFactor: 1.15 },
      samples: []
    },
    {
      id: 'p_elder',
      emoji: '👵',
      name: 'Elder',
      sex: 'female',
      age: 65,
      restingHR: 74,
      currentDay: 3, // Calibrated
      historyDays: [
        { day: 1, steps: 5200, activeCalories: 210, avgHR: 108, restingHR: 73, sleepHours: 7.2, strain: 8.2 },
        { day: 2, steps: 4900, activeCalories: 195, avgHR: 105, restingHR: 74, sleepHours: 7.4, strain: 7.9 }
      ],
      model: { hrWeight: 0.60, calWeight: 0.30, cadenceWeight: 0.10, adaptationEpochs: 2, personalEfficiencyFactor: 0.90 },
      samples: []
    }
  ];

  class HealthEngine {
    constructor(baselines = DEFAULT_BASELINES) {
      this.baselines = baselines;
      this.profiles = this.loadProfiles();
      this.activeProfileId = this.loadActiveProfileId();
      this.syncActiveState();
    }

    // --- Local Storage Multi-Profile Management (Zero-Cloud) ---

    loadProfiles() {
      if (typeof localStorage !== 'undefined') {
        const raw = localStorage.getItem(STORAGE_KEY_PROFILES);
        if (raw) {
          try {
            const parsed = JSON.parse(raw);
            if (Array.isArray(parsed) && parsed.length > 0) return parsed;
          } catch (e) { /* fallback */ }
        }
      }
      return JSON.parse(JSON.stringify(DEFAULT_PROFILES));
    }

    saveProfiles(profiles) {
      this.profiles = profiles;
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_KEY_PROFILES, JSON.stringify(this.profiles));
      }
    }

    loadActiveProfileId() {
      if (typeof localStorage !== 'undefined') {
        const id = localStorage.getItem(STORAGE_KEY_ACTIVE_ID);
        if (id && this.profiles.some(p => p.id === id)) return id;
      }
      return this.profiles[0].id;
    }

    syncActiveState() {
      let active = this.profiles.find(p => p.id === this.activeProfileId);
      if (!active) {
        active = this.profiles[0];
        this.activeProfileId = active.id;
      }
      this.profile = {
        id: active.id,
        emoji: active.emoji || '🧑',
        sex: active.sex || 'male',
        age: active.age || 30,
        restingHR: active.restingHR || 65,
        currentDay: active.currentDay || 1,
        historyDays: active.historyDays || []
      };
      this.personalModel = active.model || {
        hrWeight: 0.55,
        calWeight: 0.35,
        cadenceWeight: 0.10,
        adaptationEpochs: 0,
        personalEfficiencyFactor: 1.0
      };
      this.samples = active.samples || [];
    }

    getProfiles() {
      return this.profiles;
    }

    getActiveProfile() {
      return this.profile;
    }

    switchProfile(id) {
      if (this.profiles.some(p => p.id === id)) {
        this.activeProfileId = id;
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem(STORAGE_KEY_ACTIVE_ID, id);
        }
        this.syncActiveState();
        return this.profile;
      }
      return null;
    }

    addOrUpdateProfile({ emoji, sex, age, restingHR }) {
      const cohort = this.getCohortForAge(Number(age));
      const defaultRHR = sex === 'female' ? cohort.avg_resting_hr + 2 : cohort.avg_resting_hr;
      
      const newProfile = {
        id: 'p_' + Date.now(),
        emoji: emoji || '🧑',
        sex: sex || 'male',
        age: Math.max(12, Math.min(100, Number(age) || 30)),
        restingHR: Math.max(40, Math.min(110, Number(restingHR) || defaultRHR)),
        currentDay: 1, // Starts at Day 1 (Needs 2 days calibration)
        historyDays: [],
        model: {
          hrWeight: 0.55,
          calWeight: 0.35,
          cadenceWeight: 0.10,
          adaptationEpochs: 0,
          personalEfficiencyFactor: 1.0
        },
        samples: []
      };

      this.profiles.push(newProfile);
      this.saveProfiles(this.profiles);
      this.switchProfile(newProfile.id);
      return newProfile;
    }

    // --- Automatic Day-by-Day Timeline Progression ---

    /**
     * Advance the watch timeline by 1 day, automatically collecting 24 hours of background telemetry.
     */
    advanceDay(customActivity = null) {
      const activeIdx = this.profiles.findIndex(p => p.id === this.activeProfileId);
      if (activeIdx === -1) return null;

      const profile = this.profiles[activeIdx];
      const currentDay = profile.currentDay || 1;
      const cohort = this.getCohortForAge(profile.age);
      const isFemale = profile.sex === 'female';

      // Generate realistic automatic 24-hour day telemetry if not provided
      let dayData;
      if (customActivity) {
        dayData = {
          day: currentDay,
          steps: Math.max(500, Number(customActivity.steps) || 5000),
          activeCalories: Math.max(50, Number(customActivity.activeCalories) || 250),
          avgHR: Math.max(60, Number(customActivity.avgHR) || 120),
          restingHR: profile.restingHR || cohort.avg_resting_hr,
          sleepHours: Number((7.0 + Math.random() * 1.5).toFixed(1)),
          strain: Number((customActivity.strain || 8.0).toFixed(1))
        };
      } else {
        // Automatic background day telemetry based on age & gender
        const baseSteps = isFemale ? 7500 : 8500;
        const ageStepFactor = profile.age > 60 ? 0.65 : (profile.age > 40 ? 0.85 : 1.15);
        const autoSteps = Math.round(baseSteps * ageStepFactor + (Math.random() * 1200 - 600));

        const baseCal = isFemale ? 280 : 340;
        const autoCal = Math.round(baseCal * ageStepFactor + (Math.random() * 60 - 30));
        const autoAvgHR = Math.round(profile.restingHR + (profile.age > 50 ? 35 : 45));

        dayData = {
          day: currentDay,
          steps: autoSteps,
          activeCalories: autoCal,
          avgHR: autoAvgHR,
          restingHR: profile.restingHR,
          sleepHours: Number((isFemale ? 7.8 : 7.4).toFixed(1)),
          strain: Number((profile.age > 60 ? 8.2 : 11.5).toFixed(1))
        };
      }

      // Automatically train the local model with this day's telemetry
      this.trainWithSample({
        durationMins: 45,
        activeCalories: dayData.activeCalories,
        avgHR: dayData.avgHR,
        steps: Math.round(dayData.steps / 3),
        perceivedExertion: profile.age > 50 ? 6 : 5
      });

      profile.historyDays = profile.historyDays || [];
      profile.historyDays.push(dayData);
      profile.currentDay = Math.min(3, currentDay + 1);

      this.saveProfiles(this.profiles);
      this.syncActiveState();

      return {
        newDay: profile.currentDay,
        dayData: dayData,
        isCalibrated: profile.currentDay >= 3
      };
    }

    resetTimeline() {
      const activeIdx = this.profiles.findIndex(p => p.id === this.activeProfileId);
      if (activeIdx !== -1) {
        this.profiles[activeIdx].currentDay = 1;
        this.profiles[activeIdx].historyDays = [];
        this.profiles[activeIdx].samples = [];
        this.profiles[activeIdx].model = {
          hrWeight: 0.55,
          calWeight: 0.35,
          cadenceWeight: 0.10,
          adaptationEpochs: 0,
          personalEfficiencyFactor: 1.0
        };
        this.saveProfiles(this.profiles);
        this.syncActiveState();
      }
    }

    saveProfile(updatedFields) {
      const idx = this.profiles.findIndex(p => p.id === this.activeProfileId);
      if (idx !== -1) {
        this.profiles[idx] = { ...this.profiles[idx], ...updatedFields };
        this.saveProfiles(this.profiles);
        this.syncActiveState();
      }
      return this.profile;
    }

    savePersonalModel(model) {
      this.personalModel = model;
      const idx = this.profiles.findIndex(p => p.id === this.activeProfileId);
      if (idx !== -1) {
        this.profiles[idx].model = model;
        this.saveProfiles(this.profiles);
      }
    }

    saveSamples(samples) {
      this.samples = samples;
      const idx = this.profiles.findIndex(p => p.id === this.activeProfileId);
      if (idx !== -1) {
        this.profiles[idx].samples = samples;
        this.saveProfiles(this.profiles);
      }
    }

    // --- Cohort Baseline Resolver ---

    getCohortForAge(age) {
      const cohorts = this.baselines.age_cohorts;
      const found = cohorts.find(c => age >= c.min_age && age <= c.max_age);
      return found || cohorts[cohorts.length - 1];
    }

    // --- Gender-Aware Max HR Formula ---

    calculateMaxHR(age, sex = 'male') {
      if (this.profile && this.profile.maxHROverride) {
        return this.profile.maxHROverride;
      }
      if (sex === 'female') {
        // Gulati formula for women: 206 - (0.88 * age)
        return Math.round(206 - (0.88 * age));
      }
      // Tanaka equation for men/general: 208 - (0.7 * age)
      return Math.round(208 - (0.7 * age));
    }

    // --- Trained Baseline Ranges Calculator ---

    computeTrainedRanges() {
      const age = this.profile.age;
      const sex = this.profile.sex || 'male';
      const cohort = this.getCohortForAge(age);
      const baseRHR = this.profile.restingHR || (sex === 'female' ? cohort.avg_resting_hr + 2 : cohort.avg_resting_hr);
      const genderCalMult = sex === 'female' ? 0.88 : 1.0;
      const expectedBurnRate = Math.round(cohort.baseline_active_burn_rate_cal_hr * genderCalMult);
      const thresholds = cohort.strain_thresholds || { light: 5.5, moderate: 11.0, strenuous: 15.0 };
      const maxHR = this.calculateMaxHR(age, sex);

      const sampleCount = this.samples ? this.samples.length : 0;
      const isNew = sampleCount === 0;

      if (isNew) {
        // Newly added person: shows average ranges trained previously by the population model
        return {
          isNew: true,
          sampleCount: 0,
          statusText: 'Fresh Baseline (0 readings)',
          restingHR: {
            min: baseRHR - 5,
            max: baseRHR + 6,
            avg: baseRHR,
            unit: 'bpm'
          },
          activeCalories: {
            min: Math.round(expectedBurnRate * 0.85),
            max: Math.round(expectedBurnRate * 1.15),
            avg: expectedBurnRate,
            unit: 'cal/hr'
          },
          dailyStrain: {
            min: thresholds.light,
            max: thresholds.moderate,
            avg: Number(((thresholds.light + thresholds.moderate) / 2).toFixed(1)),
            unit: 'pts'
          },
          maxHR: maxHR
        };
      }

      // Person with collected data: adapted ranges trained by their observed samples
      const hrs = this.samples.map(s => Number(s.avgHR) || baseRHR);
      const cals = this.samples.map(s => ((Number(s.activeCalories) || 50) / Math.max(1, Number(s.durationMins) || 30)) * 60);
      
      const observedAvgHR = Math.round(hrs.reduce((a, b) => a + b, 0) / hrs.length);
      const observedAvgCal = Math.round(cals.reduce((a, b) => a + b, 0) / cals.length);

      const eff = this.personalModel.personalEfficiencyFactor || 1.0;
      const adaptedStrainAvg = Number((((thresholds.light + thresholds.moderate) / 2) / eff).toFixed(1));

      return {
        isNew: false,
        sampleCount: sampleCount,
        statusText: `${sampleCount} reading${sampleCount > 1 ? 's' : ''} collected`,
        restingHR: {
          min: Math.min(baseRHR - 5, observedAvgHR - 8),
          max: Math.max(baseRHR + 6, observedAvgHR + 8),
          avg: observedAvgHR,
          unit: 'bpm'
        },
        activeCalories: {
          min: Math.round(observedAvgCal * 0.85),
          max: Math.round(observedAvgCal * 1.15),
          avg: observedAvgCal,
          unit: 'cal/hr'
        },
        dailyStrain: {
          min: Math.max(1.0, Number((adaptedStrainAvg - 2.2).toFixed(1))),
          max: Number((adaptedStrainAvg + 2.2).toFixed(1)),
          avg: adaptedStrainAvg,
          unit: 'pts'
        },
        maxHR: maxHR
      };
    }

    // --- On-Device Personal ML Training & Online Adaptation ---

    /**
     * Collect a new reading / train the on-device model with a new local activity sample.
     * Implements online continuous learning using a gradient/moving-average step.
     */
    trainWithSample(sample) {
      const age = this.profile.age;
      const sex = this.profile.sex || 'male';
      const maxHR = this.calculateMaxHR(age, sex);
      const restingHR = this.profile.restingHR || (sex === 'female' ? this.getCohortForAge(age).avg_resting_hr + 2 : this.getCohortForAge(age).avg_resting_hr);

      // Validate inputs
      const duration = Math.max(1, Number(sample.durationMins) || 15);
      const calories = Math.max(0, Number(sample.activeCalories) || 50);
      const avgHR = Math.min(maxHR, Math.max(restingHR, Number(sample.avgHR) || restingHR + 20));
      const steps = Math.max(0, Number(sample.steps) || 500);
      const perceived = Math.min(10, Math.max(1, Number(sample.perceivedExertion) || 5));

      // Compute raw population estimate
      const cohort = this.getCohortForAge(age);
      const genderCalMult = sex === 'female' ? 0.88 : 1.0;
      const baselineHourlyCal = cohort.baseline_active_burn_rate_cal_hr * genderCalMult;
      const actualHourlyCal = (calories / duration) * 60;
      const hrReserveFraction = Math.max(0, (avgHR - restingHR) / Math.max(1, maxHR - restingHR));

      // Calculate observed efficiency vs expected
      const observedEfficiency = (actualHourlyCal / baselineHourlyCal) / Math.max(0.2, hrReserveFraction);

      // Online adaptation step (Exponential Moving Average / Soft Gradient update)
      const learningRate = 0.25; // Quick adaptation for local on-device small-batch samples
      const currentEff = this.personalModel.personalEfficiencyFactor;
      const updatedEff = currentEff * (1 - learningRate) + Math.min(2.0, Math.max(0.5, observedEfficiency)) * learningRate;

      // Adapt feature weights based on perceived exertion correlation
      // If perceived exertion is high but HR was low, increase caloric/cadence weight
      const targetStrain = (perceived / 10) * 21.0;
      const rawHRStrain = hrReserveFraction * 21.0;
      const hrDiscrepancy = targetStrain - rawHRStrain;

      let newHRWeight = this.personalModel.hrWeight - (hrDiscrepancy * 0.015);
      let newCalWeight = this.personalModel.calWeight + (hrDiscrepancy * 0.010);
      let newCadenceWeight = this.personalModel.cadenceWeight + (hrDiscrepancy * 0.005);

      // Normalize weights
      const sum = Math.max(0.01, newHRWeight + newCalWeight + newCadenceWeight);
      newHRWeight = Math.max(0.2, Math.min(0.8, newHRWeight / sum));
      newCalWeight = Math.max(0.1, Math.min(0.6, newCalWeight / sum));
      newCadenceWeight = Math.max(0.05, Math.min(0.3, 1.0 - newHRWeight - newCalWeight));

      const updatedModel = {
        hrWeight: Number(newHRWeight.toFixed(4)),
        calWeight: Number(newCalWeight.toFixed(4)),
        cadenceWeight: Number(newCadenceWeight.toFixed(4)),
        adaptationEpochs: (this.personalModel.adaptationEpochs || 0) + 1,
        personalEfficiencyFactor: Number(updatedEff.toFixed(4)),
        lastTrainedAt: new Date().toISOString()
      };

      this.savePersonalModel(updatedModel);

      // Append sample to local memory/storage
      const newSamples = [...this.samples, { ...sample, timestamp: Date.now() }];
      this.saveSamples(newSamples);

      return updatedModel;
    }

    // --- Activity & Strain Calculation ---

    /**
     * Calculates personalized health conditions & strain score.
     * Result varies from person to person based on age, resting HR, and trained personal model.
     * 
     * @param {Object} input - { durationMins, activeCalories, avgHR, steps }
     * @returns {Object} Comprehensive personalized condition results
     */
    calculateCondition(input) {
      const age = this.profile.age;
      const sex = this.profile.sex || 'male';
      const cohort = this.getCohortForAge(age);
      const maxHR = this.calculateMaxHR(age, sex);
      const restingHR = this.profile.restingHR || (sex === 'female' ? cohort.avg_resting_hr + 2 : cohort.avg_resting_hr);

      const duration = Math.max(1, Number(input.durationMins) || 30);
      const calories = Math.max(0, Number(input.activeCalories) || 0);
      const avgHR = Math.min(maxHR, Math.max(restingHR, Number(input.avgHR) || restingHR));
      const steps = Math.max(0, Number(input.steps) || 0);

      // 1. Cardiovascular Reserve Ratio
      const hrReserve = Math.max(1, maxHR - restingHR);
      const deltaHR = Math.max(0, (avgHR - restingHR) / hrReserve);

      // 2. Banister's TRIMP (Training Impulse) component adapted for age & heart rate
      const banisterGenderFactor = sex === 'female' ? 1.67 : 1.92;
      const banisterY = deltaHR * banisterGenderFactor;
      const trimpRaw = duration * deltaHR * 0.64 * Math.exp(banisterY);

      // Normalize TRIMP to 0-21 scale
      const hrStrainScore = Math.min(21.0, (trimpRaw / 140) * 21.0);

      // 3. Caloric Metabolic Strain (relative to age & sex cohort baseline)
      const genderCalMultiplier = sex === 'female' ? 0.88 : 1.0;
      const expectedBurnRate = cohort.baseline_active_burn_rate_cal_hr * genderCalMultiplier;
      const actualBurnRate = (calories / duration) * 60;
      const metabolicRatio = actualBurnRate / Math.max(1, expectedBurnRate);
      const calStrainScore = Math.min(21.0, metabolicRatio * (duration / 60) * 7.5);

      // 4. Cadence & Step Strain
      const stepRatePerMin = steps / duration;
      const stepIntensity = Math.min(2.0, stepRatePerMin / 120);
      const stepStrainScore = Math.min(21.0, stepIntensity * (duration / 60) * 6.0);

      // 5. Personal Model Synthesis (weighted by on-device trained parameters)
      const wHR = this.personalModel.hrWeight;
      const wCal = this.personalModel.calWeight;
      const wCadence = this.personalModel.cadenceWeight;
      const effFactor = this.personalModel.personalEfficiencyFactor;

      // Personalized composite strain (0.0 to 21.0 scale)
      let composite = (hrStrainScore * wHR) + (calStrainScore * wCal) + (stepStrainScore * wCadence);
      composite = composite * (cohort.exertion_coefficient / effFactor);
      const finalStrain = Math.min(21.0, Math.max(0.0, Number(composite.toFixed(1))));

      // 6. Generic population comparison (what an unpersonalized population model would say)
      const genericStrain = Math.min(21.0, Math.max(0.0, Number((
        (hrStrainScore * 0.55 + calStrainScore * 0.35 + stepStrainScore * 0.10) * cohort.exertion_coefficient
      ).toFixed(1))));

      const personalDelta = Number((finalStrain - genericStrain).toFixed(1));

      // 7. Overall Health Index (0-100 score)
      // Cardio efficiency + resting reserve + exertion tolerance
      const restingScore = Math.max(0, Math.min(100, 100 - (restingHR - 50) * 1.5));
      const strainToleranceScore = Math.max(0, Math.min(100, 100 - Math.max(0, finalStrain - 14) * 8));
      const efficiencyBonus = Math.min(15, (effFactor - 1.0) * 30);
      const overallScore = Math.round(Math.min(100, Math.max(30, (restingScore * 0.5) + (strainToleranceScore * 0.5) + efficiencyBonus)));

      // 8. Strain Classification Category
      const thresholds = cohort.strain_thresholds || { light: 5.5, moderate: 11.0, strenuous: 15.0, peak: 20.0 };
      let category = 'Rest / Recovery';
      let categoryColor = '#30d158'; // Neon Green
      if (finalStrain >= thresholds.strenuous) {
        category = 'Peak Strain';
        categoryColor = '#ff453a'; // Neon Red
      } else if (finalStrain >= thresholds.moderate) {
        category = 'Strenuous';
        categoryColor = '#ff9f0a'; // Orange
      } else if (finalStrain >= thresholds.light) {
        category = 'Moderate Activity';
        categoryColor = '#64d2ff'; // Cyan
      }

      // 9. Recommended Recovery Window
      let recoveryHours = 6;
      if (finalStrain >= 18.0) recoveryHours = 36;
      else if (finalStrain >= 14.0) recoveryHours = 24;
      else if (finalStrain >= 10.0) recoveryHours = 16;
      else if (finalStrain >= 6.0) recoveryHours = 10;

      return {
        person: {
          id: this.profile.id,
          emoji: this.profile.emoji,
          sex: sex,
          age: age,
          restingHR: restingHR
        },
        overallScore: overallScore,
        strain: finalStrain,
        category: category,
        categoryColor: categoryColor,
        genericStrain: genericStrain,
        personalDelta: personalDelta,
        adaptationEpochs: this.personalModel.adaptationEpochs,
        metrics: {
          activeCalories: calories,
          avgHR: avgHR,
          maxHR: maxHR,
          restingHR: restingHR,
          hrReserveUsedPercent: Math.round(deltaHR * 100),
          durationMins: duration,
          steps: steps
        },
        personalization: {
          ageCohort: `${cohort.min_age}-${cohort.max_age} yrs`,
          personalEfficiencyFactor: this.personalModel.personalEfficiencyFactor,
          activeWeights: {
            heartRate: Math.round(wHR * 100),
            calories: Math.round(wCal * 100),
            cadence: Math.round(wCadence * 100)
          }
        },
        recoveryHours: recoveryHours,
        trainedRanges: this.computeTrainedRanges(),
        recommendations: this.getRecommendations()
      };
    }

    // --- 2-Day Calibrated Recommendations (Sleep, Steps, Sit Still, Cardio Readiness) ---

    getRecommendations() {
      const age = this.profile.age;
      const sex = this.profile.sex || 'male';
      const cohort = this.getCohortForAge(age);
      const isFemale = sex === 'female';
      const currentDay = this.profile.currentDay || 1;
      const history = this.profile.historyDays || [];
      const isCalibrated = currentDay >= 3;

      if (!isCalibrated) {
        const cohortRHR = isFemale ? cohort.avg_resting_hr + 2 : cohort.avg_resting_hr;
        let baseStepTarget = isFemale ? 8000 : 9000;
        if (age < 30) baseStepTarget = isFemale ? 10000 : 11500;
        else if (age >= 60) baseStepTarget = isFemale ? 4800 : 5200;

        let baseSleepHours = 7.7;
        if (age < 30) baseSleepHours = 8.2;
        else if (age > 60) baseSleepHours = 7.2;
        if (isFemale) baseSleepHours += 0.25;

        const expectedBurnRate = Math.round(cohort.baseline_active_burn_rate_cal_hr * (isFemale ? 0.88 : 1.0));

        return {
          isCalibrated: false,
          currentDay: currentDay,
          dayLabel: `Day ${currentDay} of 2`,
          progressPercent: currentDay === 1 ? 40 : 80,
          statusTitle: currentDay === 1 ? 'Day 1: Establishing Baseline' : 'Day 2: Calibrating Personal Physiology',
          statusSub: 'Collecting 48h background heart and activity data. Prescriptions unlock on Day 3.',
          humanAverages: {
            cohortLabel: `${cohort.min_age}-${cohort.max_age}y ${isFemale ? 'Female' : 'Male'}`,
            restingHR: cohortRHR,
            steps: baseStepTarget,
            sleepHours: Number(baseSleepHours.toFixed(1)),
            burnRateCalHr: expectedBurnRate,
            maxSitMins: age >= 60 ? 40 : (age < 30 ? 60 : 50)
          },
          modelBaseline: {
            cohortRange: `${cohort.min_age}-${cohort.max_age}y ${isFemale ? 'Female' : 'Male'} Population Reference`,
            expectedRestingHR: cohortRHR
          }
        };
      }

      // --- Fully Calibrated (Day 3+) ---
      const observedRHRs = history.map(h => h.restingHR || this.profile.restingHR);
      const avgObservedRHR = Math.round(observedRHRs.reduce((a, b) => a + b, 0) / Math.max(1, observedRHRs.length));
      
      const observedStrains = history.map(h => h.strain || 8.0);
      const avgObservedStrain = Number((observedStrains.reduce((a, b) => a + b, 0) / Math.max(1, observedStrains.length)).toFixed(1));

      const observedSteps = history.map(h => h.steps || 7000);
      const avgObservedSteps = Math.round(observedSteps.reduce((a, b) => a + b, 0) / Math.max(1, observedSteps.length));

      // 1. Sleep Recommendation
      let baseSleepHours = 7.7;
      if (age < 30) baseSleepHours = 8.2;
      else if (age > 60) baseSleepHours = 7.2;
      
      if (isFemale) baseSleepHours += 0.25;

      let strainSleepBonus = 0;
      if (avgObservedStrain >= 13.0) strainSleepBonus = 0.75;
      else if (avgObservedStrain >= 9.0) strainSleepBonus = 0.40;

      const totalSleep = baseSleepHours + strainSleepBonus;
      const sleepH = Math.floor(totalSleep);
      const sleepM = Math.round((totalSleep - sleepH) * 60);

      // 2. Step Goal Recommendation
      let baseStepTarget = isFemale ? 8000 : 9000;
      if (age < 30) baseStepTarget = isFemale ? 10000 : 11500;
      else if (age >= 60) baseStepTarget = isFemale ? 4800 : 5200;
      else if (age >= 45) baseStepTarget = isFemale ? 6500 : 7200;

      let stepTarget = Math.round((baseStepTarget * 0.6) + (avgObservedSteps * 0.4));
      if (avgObservedStrain >= 14.0) {
        stepTarget = Math.round(stepTarget * 0.85);
      }

      // 3. Sit Still / Sedentary Threshold
      let maxSedentaryMins = 50;
      if (age >= 60) maxSedentaryMins = 40;
      else if (age < 30) maxSedentaryMins = 60;

      // 4. Cardiovascular Readiness & Condition
      const cohortRHR = isFemale ? cohort.avg_resting_hr + 2 : cohort.avg_resting_hr;
      const rhrDiff = avgObservedRHR - cohortRHR;

      let readinessScore = 85;
      let readinessStatus = 'Prime Condition';
      let readinessColor = '#30d158';
      let readinessExplanation = `2-day resting HR (${avgObservedRHR} bpm) matches optimal demographic norms.`;

      if (rhrDiff <= -4) {
        readinessScore = 94;
        readinessStatus = 'Peak Readiness';
        readinessColor = '#30d158';
        readinessExplanation = `Resting HR is ${Math.abs(rhrDiff)} bpm below model average. Cardiovascular efficiency is excellent.`;
      } else if (rhrDiff >= 5) {
        readinessScore = 72;
        readinessStatus = 'Mild Cardiac Strain';
        readinessColor = '#ff9f0a';
        readinessExplanation = `Resting HR is +${rhrDiff} bpm above demographic baseline. Prioritize restful recovery.`;
      }

      return {
        isCalibrated: true,
        currentDay: currentDay,
        dayLabel: 'Calibrated (Day 3+)',
        progressPercent: 100,
        sleep: {
          hours: sleepH,
          minutes: sleepM,
          formatted: `${sleepH}h ${sleepM}m`,
          note: `Tuned for ${age}y ${isFemale ? 'Female' : 'Male'} based on ${avgObservedStrain} avg strain recovery.`
        },
        steps: {
          target: stepTarget,
          formatted: `${stepTarget.toLocaleString()} steps`,
          note: `Calibrated from 2-day activity (${avgObservedSteps.toLocaleString()} avg) for safe cardiovascular stimulus.`
        },
        sitStill: {
          maxMins: maxSedentaryMins,
          formatted: `${maxSedentaryMins} mins max`,
          note: `Stand prompt triggers after ${maxSedentaryMins}m continuous inactivity to support circulation.`
        },
        cardioReadiness: {
          score: readinessScore,
          status: readinessStatus,
          color: readinessColor,
          explanation: readinessExplanation
        },
        modelComparison: {
          observedAvgRHR: avgObservedRHR,
          modelTrainedRHR: cohortRHR,
          rhrDelta: Number((avgObservedRHR - cohortRHR).toFixed(1)),
          avgStrain: avgObservedStrain
        }
      };
    }
  }

  return { HealthEngine, DEFAULT_BASELINES };
});
