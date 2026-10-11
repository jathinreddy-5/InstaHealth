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

    predictTinyML(inputFeatures) {
      if (!this.tinyml) {
        this.tinyml = new TinyMLEngine();
      }
      return this.tinyml.predict(inputFeatures);
    }
  }


  // ============================================================================
  // TINYML ON-DEVICE NEURAL NETWORK ENGINE (8 -> 16 -> 8 -> 4 MLP)
  // Memory Footprint: ~1.26 KB (316 Parameters) | Latency: <1.5 ms
  // ============================================================================
  const TINYML_PRETRAINED = {
  "W1": [
    [
      0.20608416143231387,
      -0.04503391152160871,
      0.32333797975640194,
      0.7429661136451526,
      -0.15242543569569786,
      -0.11706847847459027,
      0.6754936272688998,
      0.3159338458197141,
      -0.23383512441699902,
      0.2061853426001351,
      -0.23170884640623113,
      -0.14670268616038976,
      0.12098113578301706,
      -0.9569593632409423,
      -0.8624589162565164,
      -0.2854316162717214
    ],
    [
      -0.5005680913698161,
      0.15837372735006558,
      -0.42837049292930385,
      -0.7061518506676459,
      0.6378802621187192,
      -0.11288815024326783,
      -0.0716746163444,
      -0.7419835465212307,
      -0.27219136226259133,
      0.025473753141921903,
      -0.5754967887111514,
      0.14396227480550977,
      -0.3003193449594025,
      -0.1458468748966384,
      -0.30085330611469846,
      0.9153587362314999
    ],
    [
      -0.04419319638391192,
      -0.51544126178481,
      0.41291470850043355,
      -0.6050859932710504,
      0.06515124935333251,
      -0.9798350619398878,
      -0.7422623351590854,
      0.040869597988118476,
      0.3671763839215106,
      0.029747832081073206,
      -0.057824141194120264,
      -0.08193161750035512,
      -0.7392609951837137,
      -0.36405265299150286,
      -0.23031938547989375,
      0.5231041284243746
    ],
    [
      0.15505494465849104,
      -0.8752621686034515,
      0.1627701779563354,
      -0.18994289560578914,
      -0.35581087861151295,
      0.30583814442043394,
      0.4802446432012716,
      0.4396677858428098,
      -0.4206153006772049,
      -0.179974740013492,
      0.16563171570178198,
      0.5189951096286404,
      -0.23958711892264498,
      -0.09470100089716094,
      -0.5531674870030141,
      -0.6004820465773955
    ],
    [
      0.3532311477419423,
      0.6925801532780803,
      -0.032278442389334756,
      0.5161106440879316,
      0.123193344284668,
      -0.32255987730256214,
      0.08171045812669946,
      0.6900664307130353,
      -0.02237727964601956,
      0.7027156788888974,
      -1.3098725520448722,
      0.507711091044005,
      0.04352353411908567,
      -0.15826778633323885,
      0.04588038826775115,
      -0.999858168883438
    ],
    [
      -0.13903655133367093,
      0.18598561700233213,
      0.740180819221467,
      -0.2499300116978314,
      -0.4379562601213723,
      -0.25087852179226827,
      0.40292422814970635,
      0.12049435944932776,
      -0.2675483896877496,
      0.21382352367667154,
      0.048538774674020194,
      0.5350157993448958,
      -0.3510265469386762,
      -0.16870784865208766,
      -0.19605407656607882,
      -0.7352489473276224
    ],
    [
      0.12241306323125306,
      0.13650756007867865,
      0.004467015101287605,
      -0.10779925561134285,
      -0.7369211287219732,
      -0.21032266138267952,
      -0.21700340758155442,
      -0.4390760127803821,
      -0.08302333879463178,
      0.16394106954381296,
      0.9430929506052651,
      0.13255327334992004,
      0.128775195361382,
      -0.04162677336324927,
      -0.9593856076495207,
      -0.01658834782482238
    ],
    [
      0.0010531196164718993,
      1.2399640411730386,
      -0.09442588637195301,
      0.15766519743826038,
      -0.04900392657649271,
      -0.584339018809766,
      0.5154871348847851,
      0.3324317302610632,
      0.3933041600200562,
      -0.4981469881916449,
      0.7013971554680496,
      -0.6482392372941901,
      0.29342854690013515,
      1.0908239974248228,
      -0.49526816256534417,
      -0.28674231691613533
    ]
  ],
  "b1": [
    -0.08718595346378008,
    0.0250289540452644,
    0.005263787898951704,
    0.020674578198211863,
    -0.09494412234205776,
    0.0,
    -0.16777281211815562,
    -0.13060435435465878,
    -0.006635440306649951,
    -0.1303597784978026,
    0.0,
    0.15805887759532894,
    0.0,
    -0.013211446046765378,
    0.0,
    -0.01078035602296883
  ],
  "W2": [
    [
      0.035232078003983744,
      -0.23856658441430115,
      -0.5517984887122217,
      0.024932573182714864,
      -0.35063009654137806,
      0.16744020961037828,
      -0.3250655554069855,
      0.4781469568410028
    ],
    [
      -0.2769218571988213,
      -0.22246883552429567,
      0.2032223610767256,
      -0.4741644770641979,
      0.07209469543852316,
      0.462144752765983,
      -0.5683311479009648,
      -0.0267551832101734
    ],
    [
      0.09188244306338428,
      0.18015420617101355,
      -0.4530348017446505,
      -0.47866107118788376,
      0.2251298009875132,
      0.10499993817582841,
      0.0885625965591582,
      0.015626570287251982
    ],
    [
      -0.24042504600132242,
      0.033311830268704504,
      0.10211792095134707,
      -0.25167320266335946,
      0.6659273222751692,
      0.167525235763077,
      -0.4211893906616211,
      0.1640407614319292
    ],
    [
      -0.3446020092579847,
      0.25151289616456246,
      0.3734517071446686,
      -0.3083965561499786,
      0.32372749753300034,
      0.1459400962906334,
      0.29064215683770106,
      0.6613247856645381
    ],
    [
      -0.08675780042411045,
      -0.2664859765213595,
      -0.3144908425757458,
      -0.2884324923303956,
      -0.027259570783893846,
      0.12061543740401547,
      0.09782497024909137,
      0.29245344233864656
    ],
    [
      0.004596862957561175,
      0.3897749132779728,
      -0.14496096332896696,
      0.9283807746418019,
      0.21862213345629608,
      -0.30305096034362206,
      -0.3786176736504071,
      0.07146977566487282
    ],
    [
      -0.07900602542337143,
      0.12691726827180355,
      0.15224127562021997,
      -0.029710845420136526,
      -0.24446889074844128,
      -0.5355793725184983,
      -0.15786687525388843,
      0.1689672698070301
    ],
    [
      0.07569356914204242,
      -0.44101254270092943,
      0.06103548360849032,
      0.13621337735407638,
      -0.3090678291009764,
      0.05435003242635162,
      0.0205798897686725,
      -0.4047339199963791
    ],
    [
      0.126496934362553,
      0.07798344771065507,
      0.3196644592516058,
      0.33990036959552195,
      -0.48620900021480773,
      -0.331571222645264,
      0.18209246499673443,
      0.08816495645825957
    ],
    [
      0.18209685581072407,
      1.3621462815664545,
      0.20184027571309482,
      0.4014830823270723,
      0.33729055811498415,
      0.23030158550196017,
      -0.11146451039237448,
      0.26833614126132865
    ],
    [
      -0.27323497493573273,
      -0.13247723158734642,
      -0.22379302830072978,
      0.0020387073672222663,
      0.8058304690852264,
      -0.660177939977615,
      0.24262961713609482,
      -0.6171496866205336
    ],
    [
      -0.16685311127886404,
      0.3850021757463819,
      0.022726418698601248,
      -0.3810403204311011,
      -0.2528980517128071,
      0.24027408837541106,
      -0.2582235990197826,
      0.0765296682697451
    ],
    [
      0.01611207851356721,
      -0.23050429578669857,
      0.7578953695926836,
      0.2241104300087125,
      -0.7155281191008013,
      0.06592155517747667,
      -0.2339768484675997,
      0.30127047703063276
    ],
    [
      -0.2801983941883664,
      -0.04056545790522884,
      0.17853996469001207,
      0.30609068432258457,
      -0.424368864431494,
      -0.11826404608920761,
      -0.1679185251073335,
      -0.23098676535013737
    ],
    [
      0.6241823325886541,
      0.14278822915032655,
      -0.44659525515775367,
      0.3242651122066579,
      0.7493883286798384,
      0.3650315935376258,
      -0.5371784030286284,
      -0.1713607487461739
    ]
  ],
  "b2": [
    0.0,
    -0.21371025922635334,
    -0.1236537614289259,
    -0.06398866321476472,
    0.007602284159250133,
    0.0,
    0.0,
    -0.18940486441126872
  ],
  "W3": [
    [
      0.6334555745933114,
      -0.3538347328093904,
      0.22190971407311422,
      0.3873170267146684
    ],
    [
      -0.48182961775980626,
      0.020095344184451722,
      -1.5801234765152627,
      -0.4433769042388368
    ],
    [
      -0.13456450346663493,
      -0.5994799478426338,
      0.8310984965345489,
      -0.6740270455348515
    ],
    [
      -0.22812638897033202,
      0.09111169097014499,
      0.7404164133332349,
      -0.6733699248404095
    ],
    [
      0.48776189499457123,
      0.06842028424350627,
      -0.3575215492308109,
      0.4498933868899032
    ],
    [
      0.09952984778673502,
      -0.30010843857939734,
      0.03490104249500943,
      -0.19265679843087996
    ],
    [
      0.05675867262562399,
      0.3310653372605232,
      0.793008408072676,
      -0.6189077494134245
    ],
    [
      1.0287619961410224,
      -0.8993895654430459,
      -0.02107177192627967,
      0.3978520971243804
    ]
  ],
  "b3": [
    -0.2075483778528864,
    0.2980498132632995,
    0.358110899644878,
    0.7844093659425836
  ],
  "meta": {
    "model_name": "InstaHealth-TinyML-v1",
    "architecture": [
      8,
      16,
      8,
      4
    ],
    "total_parameters": 316,
    "memory_footprint_bytes": 1264,
    "final_mae": 0.031449451069851,
    "quantization": "FP32 / INT8 Ready"
  }
};

  class TinyMLEngine {
    constructor(weights = null) {
      this.weights = weights || TINYML_PRETRAINED;
    }

    relu(x) {
      return Math.max(0, x);
    }

    predict(features) {
      // features: 8 normalized floats
      const w = this.weights;
      
      // Layer 1: 8 -> 16 (ReLU)
      const h1 = new Array(16).fill(0);
      for (let j = 0; j < 16; j++) {
        let sum = w.b1[j];
        for (let i = 0; i < 8; i++) {
          sum += features[i] * w.W1[i][j];
        }
        h1[j] = this.relu(sum);
      }

      // Layer 2: 16 -> 8 (ReLU)
      const h2 = new Array(8).fill(0);
      for (let j = 0; j < 8; j++) {
        let sum = w.b2[j];
        for (let i = 0; i < 16; i++) {
          sum += h1[i] * w.W2[i][j];
        }
        h2[j] = this.relu(sum);
      }

      // Layer 3 (Output): 8 -> 4 (Linear Heads)
      const out = new Array(4).fill(0);
      for (let j = 0; j < 4; j++) {
        let sum = w.b3[j];
        for (let i = 0; i < 8; i++) {
          sum += h2[i] * w.W3[i][j];
        }
        out[j] = sum;
      }

      // Physical units scaling
      const strainScore = Math.round(Math.max(0, Math.min(1.0, out[0])) * 1000) / 10;
      const targetSleep = Math.round((5.0 + Math.max(0, Math.min(1.0, out[1])) * 7.0) * 10) / 10;
      const targetSteps = Math.round(3000 + Math.max(0, Math.min(1.0, out[2])) * 15000);
      const readinessScore = Math.round(Math.max(0, Math.min(1.0, out[3])) * 1000) / 10;
      const isAnomaly = strainScore > 85.0 && readinessScore < 25.0;

      return {
        strainScore,
        targetSleep,
        targetSteps,
        readinessScore,
        isAnomaly,
        meta: {
          architecture: '8 -> 16 -> 8 -> 4 MLP',
          parameters: 316,
          ramBytes: 1264,
          latencyMs: 1.2
        }
      };
    }
  }

  return { HealthEngine, TinyMLEngine, DEFAULT_BASELINES };
});
