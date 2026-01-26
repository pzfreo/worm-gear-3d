/**
 * TypeScript type definitions for Worm Gear Design API v2.0
 *
 * Generated from JSON Schema: schemas/wormgear-design-v2.0.json
 *
 * This file defines the contract between JavaScript and Python
 * for the worm gear calculator API.
 */

// ============================================================
// Enums
// ============================================================

/** Thread/gear hand direction */
export type Hand = "right" | "left";

/** Tooth profile per DIN 3975 */
export type WormProfile = "ZA" | "ZK" | "ZI";

/** Worm geometry type */
export type WormType = "cylindrical" | "globoid";

/** Validation message severity */
export type MessageSeverity = "error" | "warning" | "info";

/** Anti-rotation feature type */
export type AntiRotationType = "none" | "DIN6885" | "ddcut";

/** Hub type for wheel */
export type HubType = "flush" | "extended" | "flanged";

/** Bore type for features */
export type BoreType = "none" | "auto" | "custom";

/** Design calculation mode */
export type DesignMode = "module" | "centre_distance" | "wheel" | "envelope";

// ============================================================
// Component Types
// ============================================================

/** Worm dimensional parameters */
export interface WormParams {
  module_mm: number;
  num_starts: number;
  pitch_diameter_mm: number;
  tip_diameter_mm: number;
  root_diameter_mm: number;
  lead_mm: number;
  lead_angle_deg: number;
  addendum_mm: number;
  dedendum_mm: number;
  thread_thickness_mm: number;
  hand: Hand;
  profile_shift?: number;
  type?: WormType;
  throat_reduction_mm?: number;
  throat_curvature_radius_mm?: number;
  length_mm?: number;
}

/** Wheel dimensional parameters */
export interface WheelParams {
  module_mm: number;
  num_teeth: number;
  pitch_diameter_mm: number;
  tip_diameter_mm: number;
  root_diameter_mm: number;
  throat_diameter_mm: number;
  helix_angle_deg: number;
  addendum_mm: number;
  dedendum_mm: number;
  profile_shift?: number;
  width_mm?: number;
}

/** Assembly parameters */
export interface AssemblyParams {
  centre_distance_mm: number;
  pressure_angle_deg: number;
  backlash_mm: number;
  hand: Hand;
  ratio: number;
  efficiency_percent?: number | null;
  self_locking?: boolean | null;
}

/** Manufacturing/generation parameters */
export interface ManufacturingParams {
  profile?: WormProfile;
  virtual_hobbing?: boolean;
  hobbing_steps?: number;
  throated_wheel?: boolean;
  sections_per_turn?: number;
  worm_length_mm?: number;
  wheel_width_mm?: number;
}

/** Set screw specification */
export interface SetScrewSpec {
  size: string;
  count?: number;
}

/** Hub specification (wheel only) */
export interface HubSpec {
  type?: HubType;
  length_mm?: number;
  flange_diameter_mm?: number;
  flange_thickness_mm?: number;
  bolt_holes?: number;
  bolt_diameter_mm?: number;
}

/** Manufacturing features for a part */
export interface PartFeatures {
  bore_diameter_mm?: number;
  anti_rotation?: AntiRotationType;
  ddcut_depth_percent?: number;
  set_screw?: SetScrewSpec;
  hub?: HubSpec;
}

/** Manufacturing features for worm and wheel */
export interface Features {
  worm?: PartFeatures;
  wheel?: PartFeatures;
}

/** A validation message with severity and suggestion */
export interface ValidationMessage {
  severity: MessageSeverity;
  code: string;
  message: string;
  suggestion?: string | null;
}

/** Design validation results */
export interface ValidationResult {
  valid: boolean;
  errors: ValidationMessage[];
  warnings: ValidationMessage[];
  infos: ValidationMessage[];
}

// ============================================================
// Main Design Type
// ============================================================

/**
 * Complete worm gear design output from calculator.
 *
 * This is the main data structure exchanged between JavaScript
 * and the Python calculator via Pyodide.
 */
export interface WormGearDesign {
  schema_version: "2.0";
  worm: WormParams;
  wheel: WheelParams;
  assembly: AssemblyParams;
  manufacturing?: ManufacturingParams;
  features?: Features;
  validation?: ValidationResult;
}

// ============================================================
// Calculator Inputs Type
// ============================================================

/**
 * User inputs to the worm gear calculator.
 *
 * This structure enables save/load of calculator configurations.
 * Use this to persist user's input settings across sessions.
 */
export interface CalculatorInputs {
  schema_version: "2.0";
  design_mode: DesignMode;

  // Core parameters (availability depends on design_mode)
  module_mm?: number | null;
  ratio: number;
  num_starts?: number;
  centre_distance_mm?: number | null;
  wheel_od_mm?: number | null;
  worm_od_mm?: number | null;
  worm_pitch_diameter_mm?: number | null;
  target_lead_angle_deg?: number;

  // Configuration
  pressure_angle_deg?: number;
  backlash_mm?: number;
  hand?: Hand;
  profile_shift?: number;

  // Manufacturing
  profile?: WormProfile;
  worm_type?: WormType;
  throat_reduction_mm?: number;
  wheel_throated?: boolean;
  virtual_hobbing?: boolean;
  hobbing_steps?: number;

  // Bore features - worm
  worm_bore_type?: BoreType;
  worm_bore_mm?: number | null;
  worm_anti_rotation?: AntiRotationType;

  // Bore features - wheel
  wheel_bore_type?: BoreType;
  wheel_bore_mm?: number | null;
  wheel_anti_rotation?: AntiRotationType;
}

// ============================================================
// Helper Types
// ============================================================

/** Default calculator inputs for a new session */
export const DEFAULT_CALCULATOR_INPUTS: CalculatorInputs = {
  schema_version: "2.0",
  design_mode: "module",
  module_mm: 2.0,
  ratio: 30,
  num_starts: 1,
  target_lead_angle_deg: 7.0,
  pressure_angle_deg: 20.0,
  backlash_mm: 0.05,
  hand: "right",
  profile_shift: 0,
  profile: "ZA",
  worm_type: "cylindrical",
  throat_reduction_mm: 0,
  wheel_throated: false,
  virtual_hobbing: false,
  hobbing_steps: 18,
  worm_bore_type: "none",
  worm_anti_rotation: "none",
  wheel_bore_type: "none",
  wheel_anti_rotation: "none",
};
