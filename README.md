# TestPatterns

Professional test patterns in SVG format for display, camera, and monitor calibration. These patterns are vector-based and scale to any resolution without quality loss.

## Pattern Collection

### Broadcast Standards

#### 1. SMPTE Color Bars - 75% (`smpte_color_bars.svg`)
- **Purpose**: Standard broadcast color calibration (SMPTE RP 219-2:2002)
- **Features**: 75% amplitude color bars with PLUGE pattern
- **Use Cases**:
  - Broadcast equipment calibration (most common variant)
  - Video monitor color accuracy testing
  - Hue and saturation verification
  - Signal level checking

#### 2. SMPTE Color Bars - 100% (`smpte_color_bars_100.svg`)
- **Purpose**: Full amplitude broadcast color calibration (SMPTE RP 219-2:2002)
- **Features**: 100% amplitude color bars with PLUGE pattern
- **Use Cases**:
  - Testing equipment headroom and clipping
  - Maximum saturation color accuracy
  - Peak signal level verification
  - High-end broadcast equipment calibration

#### 3. EBU Color Bars (`ebu_color_bars.svg`)
- **Purpose**: European broadcast standard (PAL/EBU)
- **Features**: Full height 100% saturated color bars
- **Use Cases**:
  - PAL video equipment calibration
  - European broadcast standards compliance
  - Color reproduction testing

### Brightness and Contrast

#### 4. Grayscale Steps (`grayscale_steps.svg`)
- **Purpose**: Gamma, brightness, and contrast calibration
- **Features**: 21 discrete steps from 0% to 100% in 5% increments
- **Use Cases**:
  - Monitor gamma calibration
  - Brightness/contrast adjustment
  - Shadow and highlight detail verification
  - Print calibration

#### 5. Smooth Gradients (`gradient_smooth.svg`)
- **Purpose**: Smooth color transitions and gamma testing
- **Features**: Linear gradients for grayscale, RGB, and CMY channels
- **Use Cases**:
  - Detecting banding artifacts
  - Verifying smooth color transitions
  - Color channel response testing
  - Gamma curve analysis

#### 6. Dynamic Range Test (`dynamic_range.svg`)
- **Purpose**: Camera and monitor dynamic range testing
- **Features**: 11 stops from -5 to +5 around 18% middle gray
- **Use Cases**:
  - Camera exposure latitude testing
  - HDR capability verification
  - Monitor dynamic range assessment
  - Exposure calibration

#### 7. PLUGE Pattern (`pluge.svg`)
- **Purpose**: Black level and brightness calibration
- **Features**: Picture Line-Up Generation Equipment standard pattern
- **Use Cases**:
  - Black level calibration (brightness control)
  - Distinguishing black from below-black
  - Professional monitor setup
  - Home theater calibration

### Resolution and Sharpness

#### 8. Resolution Chart (`resolution_chart.svg`)
- **Purpose**: Sharpness and resolution testing
- **Features**: Multiple line widths, checkerboards, corner markers
- **Use Cases**:
  - Lens sharpness testing
  - Focus verification across frame
  - Optical resolution measurement
  - Compression artifact detection

#### 9. Zone Plate (`zone_plate.svg`)
- **Purpose**: Resolution limits and aliasing detection
- **Features**: Concentric circles with decreasing spacing
- **Use Cases**:
  - Identifying resolution limits
  - Detecting aliasing artifacts
  - Moiré pattern detection
  - Sensor/optics testing

#### 10. Focus Chart (`focus_chart.svg`)
- **Purpose**: Focus accuracy and uniformity testing
- **Features**: Siemens star patterns (center and corners)
- **Use Cases**:
  - Autofocus accuracy testing
  - Manual focus verification
  - Lens sharpness across frame
  - Field curvature detection

### Geometry and Distortion

#### 11. Grid/Crosshatch (`grid_crosshatch.svg`)
- **Purpose**: Geometry, linearity, and distortion testing
- **Features**: Regular grid with diagonal reference lines
- **Use Cases**:
  - Monitor geometry calibration
  - Lens distortion detection
  - Aspect ratio verification
  - Projector alignment

#### 12. Circular Grid (`circular_grid.svg`)
- **Purpose**: Lens distortion testing
- **Features**: Concentric circles and radial lines
- **Use Cases**:
  - Barrel distortion detection
  - Pincushion distortion detection
  - Lens quality assessment
  - Wide-angle lens testing

#### 13. Checkerboard (`checkerboard.svg`)
- **Purpose**: High-contrast pattern for multiple tests
- **Features**: 16x9 checkerboard with 120px squares
- **Use Cases**:
  - Focus and convergence testing
  - Compression artifact detection
  - Aliasing detection
  - Motion blur testing (when animated)

### Color Calibration

#### 14. Color Checker Chart (`color_checker.svg`)
- **Purpose**: Camera color calibration
- **Features**: 24-patch reference chart (similar to X-Rite ColorChecker)
- **Use Cases**:
  - Camera color profiling
  - Color reproduction accuracy
  - White balance verification
  - Post-processing color reference

#### 15. White Balance Gray Card (`white_balance_gray_card.svg`)
- **Purpose**: Camera white balance calibration
- **Features**: 18% gray card with white and black references
- **Use Cases**:
  - Setting custom white balance
  - Exposure metering reference
  - Color temperature verification
  - Neutral reference for grading

### Alignment and Registration

#### 16. Alignment and Registration (`alignment_registration.svg`)
- **Purpose**: Framing, positioning, and aspect ratio testing
- **Features**: Safe area guides, registration marks, crosshairs
- **Use Cases**:
  - Camera framing and composition
  - Multi-camera alignment
  - Action/title safe area verification
  - Aspect ratio confirmation
  - Video overlay alignment

## Usage Guidelines

### For Monitor Calibration

1. Start with **PLUGE** to set black level (brightness)
2. Use **SMPTE Color Bars** or **Grayscale Steps** to adjust contrast
3. Verify with **Smooth Gradients** for banding
4. Check **Grid/Crosshatch** for geometry
5. Use **Resolution Chart** to verify sharpness

### For Camera Calibration

1. Use **White Balance Gray Card** to set white balance
2. Verify exposure with **Dynamic Range Test**
3. Check **Color Checker Chart** for color accuracy
4. Test focus with **Focus Chart**
5. Check lens distortion with **Circular Grid**
6. Verify sharpness with **Resolution Chart**

### For Video Production

1. Use **Alignment and Registration** for framing
2. Check **SMPTE Color Bars** for signal integrity
3. Verify **Resolution Chart** for sharpness
4. Use **Checkerboard** for compression testing
5. Check **Grid/Crosshatch** for aspect ratio

## Technical Specifications

- **Format**: SVG (Scalable Vector Graphics)
- **Native Resolution**: 1920x1080 (Full HD / 1080p)
- **Aspect Ratio**: 16:9
- **Color Space**: sRGB
- **Scaling**: Infinite (vector-based)

## Viewing Recommendations

- **Display**: Use accurate, calibrated monitor when possible
- **Browser**: Modern browsers with full SVG support (Chrome, Firefox, Safari, Edge)
- **Lighting**: Dim ambient lighting for monitor calibration
- **Distance**: Appropriate viewing distance (typically 1.5-3x screen height)
- **Full Screen**: View patterns in full-screen mode for best results

## File Descriptions

| File | Size | Primary Use |
|------|------|-------------|
| `smpte_color_bars.svg` | ~ | Broadcast color standard (75%) |
| `smpte_color_bars_100.svg` | ~ | Broadcast color standard (100%) |
| `ebu_color_bars.svg` | ~ | European broadcast standard |
| `grayscale_steps.svg` | ~ | Gamma and contrast |
| `gradient_smooth.svg` | ~ | Smooth gradients |
| `dynamic_range.svg` | ~ | Exposure latitude |
| `pluge.svg` | ~ | Black level calibration |
| `resolution_chart.svg` | ~ | Sharpness testing |
| `zone_plate.svg` | ~ | Aliasing detection |
| `focus_chart.svg` | ~ | Focus accuracy |
| `grid_crosshatch.svg` | ~ | Geometry testing |
| `circular_grid.svg` | ~ | Lens distortion |
| `checkerboard.svg` | ~ | Multiple tests |
| `color_checker.svg` | ~ | Color calibration |
| `white_balance_gray_card.svg` | ~ | White balance |
| `alignment_registration.svg` | ~ | Framing and alignment |

## Tips for Best Results

### Monitor Calibration
- Warm up display for 20-30 minutes before calibration
- Use native resolution of your display
- Disable dynamic contrast, motion smoothing, and image enhancement
- Set color temperature to D65 (6500K) if available

### Camera Calibration
- Ensure even, neutral lighting when using gray card
- Fill frame completely with test pattern
- Use tripod for stable, repeatable results
- Test at various focal lengths and apertures

### General Testing
- View patterns at 100% zoom when possible
- Compare results across different devices
- Document settings for repeatable calibration
- Re-calibrate periodically (every 3-6 months)

## License

These test patterns are provided for professional calibration and testing purposes.

## Contributing

For issues or improvements, please submit via the project repository.

---

**Note**: These patterns are designed for professional use in video production, photography, display calibration, and equipment testing. They conform to industry standards where applicable (SMPTE, EBU, etc.).
