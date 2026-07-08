export interface ProductData {
  title: string;
  category: string;
  desc: string;
  specs: Record<string, string>;
  features: string[];
}

export const productData: Record<string, ProductData> = {
  '19-welding-positioner-wp1': {
    title: 'Welding Positioner WP1',
    category: 'positioner',
    desc: 'The WP1 is a compact 1-ton capacity welding positioner designed for small to medium workpiece rotation during welding. Ideal for pipe flanges, small vessels, and component fabrication.',
    specs: { 'Capacity': '1 ton', 'Table Diameter': '800 mm', 'Tilt Angle': '0-90°', 'Rotation Speed': '0.1-1.0 rpm', 'Motor Power': '0.75 kW', 'Table Height': '900 mm', 'Control': 'Foot pedal + pendant' },
    features: ['Compact footprint for small workshops', 'Variable speed control via VFD', '90° manual tilt with locking pin', 'Foot pedal for hands-free operation', 'CE-certified motor and reducer']
  },
  '32-small-pipe-rotator-pr1a': {
    title: 'Small Pipe Rotator PR1A',
    category: 'turning rolls',
    desc: 'PR1A small pipe rotator designed for precision rotation of small diameter pipes and tubes during welding. Features self-aligning rollers and adjustable wheelbase.',
    specs: { 'Capacity': '1 ton', 'Pipe Diameter': '60-800 mm', 'Wheel Type': 'Rubber', 'Speed Range': '100-1000 mm/min', 'Motor': '0.37 kW x 2', 'Control': 'Hard-wired pendant' },
    features: ['Self-aligning roller design', 'Adjustable wheelbase for different diameters', 'Rubber wheels protect workpiece surface', 'Forward/reverse rotation control', 'Compact and portable']
  },
  '46-h-beam-assembling-product-machine-z15': {
    title: 'H-Beam Assembling Machine Z15',
    category: 'h beam',
    desc: 'The Z15 H-beam assembly machine features hydraulic clamping and precision alignment for web and flange assembly prior to welding. Suitable for H-beam production lines up to 1500mm web height.',
    specs: { 'Web Height': '200-1500 mm', 'Flange Width': '200-800 mm', 'Beam Length': '6-15 m', 'Clamping Force': '15 ton', 'Hydraulic Pressure': '20 MPa', 'Assembly Speed': '1-3 m/min' },
    features: ['Hydraulic clamping for precise alignment', 'Motorized roller conveyor integration', 'Digital readout for alignment position', 'Quick-change tooling for different sizes', 'Centralized lubrication system']
  },
  '35-boom-and-column-welding-wm': {
    title: 'Boom & Column Welding WM',
    category: 'boom&column',
    desc: 'Standard welding boom and column manipulator series for automated longitudinal and circumferential welding. The WM series provides stable, vibration-free welding head positioning across the full work envelope.',
    specs: { 'Horizontal Reach': '3-10 m', 'Vertical Stroke': '3-10 m', 'Column Rotation': '360° manual / 180° motorized', 'Boom Travel Speed': '100-1200 mm/min', 'Weight Capacity': 'Up to 200 kg on cross slide' },
    features: ['Rigid box-section column design', 'VFD-controlled smooth travel', 'Wire feeder platform on cross slide', 'Integrated cable management system', 'Optional motorized column rotation']
  },
  '71-robot-welding-positioner-double-axis-p-type-sets': {
    title: 'Robot Welding Positioner — Double Axis P-Type',
    category: 'robot',
    desc: 'Dual-axis P-type positioner sets designed for integration with 6-axis industrial welding robots. Headstock and tailstock configuration provides stable rotation and tilt for complex workpiece positioning.',
    specs: { 'Capacity': '500-3000 kg', 'Rotation Axis': '360° continuous', 'Tilt Axis': '±135°', 'Repeatability': '±0.05 mm', 'Compatible Robots': 'ABB, FANUC, KUKA, Yaskawa', 'Communication': 'EtherCAT / ProfiNet' },
    features: ['Synchronized headstock/tailstock motion', 'External axis controlled by robot controller', 'Hollow shaft for gas and sensor routing', 'Safety interlock with robot cell', 'Precision harmonic drive gearboxes']
  },
  '42-hardfacing-welding-machine-dh50': {
    title: 'Hardfacing Welding Machine DH50',
    category: 'automation',
    desc: 'The DH50 is a heavy-duty hardfacing machine for welding wear-resistant layers onto large industrial rollers, shafts, and cylindrical components up to 50 tons.',
    specs: { 'Max Workpiece Weight': '50 ton', 'Max Workpiece Diameter': '3000 mm', 'Max Workpiece Length': '10 m', 'Welding Process': 'SAW / Open Arc', 'Deposition Rate': 'Up to 25 kg/h', 'Control System': 'PLC + HMI touchscreen' },
    features: ['Automatic step-over control', 'Temperature monitoring with interpass cooling', 'Flux recovery and recycling system', 'Programmable weld patterns', 'Remote diagnostics capability']
  },
  '47-h-beam-welding-machine': {
    title: 'H-Beam Welding Machine',
    category: 'h beam',
    desc: 'Twin-arc submerged arc welding machine for simultaneous fillet welding of H-beam web-to-flange joints. One-pass welding of both sides for maximum productivity.',
    specs: { 'Web Height': '200-2000 mm', 'Flange Width': '200-1000 mm', 'Welding Speed': '300-1200 mm/min', 'Wire Diameter': '3.2-5.0 mm', 'Power Source': '2 x 1250A DC', 'Flux System': 'Automatic recovery' },
    features: ['Twin-arc simultaneous welding both sides', 'Laser seam tracking optional', 'Automatic flux feeding and recovery', 'Remote wire feed system', 'Parameter memory for 100 beam profiles']
  },
};
