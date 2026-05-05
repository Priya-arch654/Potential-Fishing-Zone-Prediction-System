---
name: Maritime Intelligence System
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#42474d'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#73777e'
  outline-variant: '#c3c7ce'
  surface-tint: '#406182'
  primary: '#001629'
  on-primary: '#ffffff'
  primary-container: '#002b49'
  on-primary-container: '#7293b6'
  inverse-primary: '#a8caef'
  secondary: '#006a65'
  on-secondary: '#ffffff'
  secondary-container: '#76f3ea'
  on-secondary-container: '#006f69'
  tertiary: '#2c0800'
  on-tertiary: '#ffffff'
  tertiary-container: '#4f1500'
  on-tertiary-container: '#e66c3f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#cfe5ff'
  primary-fixed-dim: '#a8caef'
  on-primary-fixed: '#001d34'
  on-primary-fixed-variant: '#274969'
  secondary-fixed: '#79f6ed'
  secondary-fixed-dim: '#59dad1'
  on-secondary-fixed: '#00201e'
  on-secondary-fixed-variant: '#00504c'
  tertiary-fixed: '#ffdbcf'
  tertiary-fixed-dim: '#ffb59c'
  on-tertiary-fixed: '#380c00'
  on-tertiary-fixed-variant: '#822800'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-bold:
    fontFamily: Work Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-mono:
    fontFamily: Work Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: -0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
  xl: 48px
  gutter: 20px
  margin: 24px
---

## Brand & Style

The design system is engineered to bridge the gap between rugged maritime utility and sophisticated AI data analysis. It targets a dual audience: commercial fishermen requiring immediate, glanceable insights in high-glare environments, and data analysts performing deep-dive trend monitoring. 

The style is **Modern Corporate with a Minimalist focus**, utilizing a card-based architecture to organize complex data into digestible modules. The aesthetic evokes the vastness and clarity of the open sea—clean, professional, and trustworthy. By prioritizing functional whitespace and a "calm" interface, the design system reduces cognitive load during high-stakes maritime operations.

## Colors

The palette is derived from maritime environments to create an intuitive user experience. 
- **Primary (Deep Ocean Blue):** Used for navigation, primary buttons, and heavy text to establish authority and depth.
- **Secondary (Seafoam Green):** Applied to secondary actions, data visualizations, and success states, providing a refreshing contrast to the deep blues.
- **Tertiary (Coral):** Reserved strictly for high-priority alerts and critical warnings to ensure immediate visual detection.
- **Neutral/Surface:** A "Clear White" (#FFFFFF) is used for cards to separate them from the light grayish-blue background (#F8FAFC), ensuring maximum legibility.
- **Map Zones:** A high-contrast traffic light system (Green, Yellow, Red) is used specifically for probability zones to ensure rapid decision-making.

## Typography

This design system utilizes **Inter** for its neutral, highly legible characteristics, making it ideal for the high-density data typical of maritime AI. For technical data points—such as coordinates, depth, and timestamps—**Work Sans** is used to provide a more grounded, professional feel with superior character distinction.

Hierarchy is enforced through weight and scale. Essential data points (like "Catch Probability" or "Vessel Speed") should use the `data-mono` or `title-sm` styles to stand out within card layouts. All caps should be reserved for `label-bold` to denote categories or metadata.

## Layout & Spacing

The design system employs a **12-column fluid grid** for desktop and a single-column stack for mobile devices. The rhythm is based on a 4px baseline, ensuring all elements align to a consistent vertical and horizontal scale.

- **Margins:** A minimum 24px margin is maintained around the viewport to prevent "edge-crowding," which is critical for visibility on vibration-prone vessel screens.
- **Gaps:** Use `md` (24px) spacing between primary cards and `sm` (16px) for elements within a card.
- **Whitespace:** Ample padding is required within cards to ensure data points do not bleed into one another, facilitating quick scanning.

## Elevation & Depth

Visual hierarchy is achieved through **Ambient Shadows** and **Tonal Layering**. 

- **Level 0 (Background):** The base canvas uses the Neutral hex to minimize glare.
- **Level 1 (Cards):** Pure white surfaces with a soft, diffused shadow (Blur: 15px, Y: 4px, Opacity: 6% Primary Color). This "lifts" the data from the map or background.
- **Level 2 (Modals/Active States):** Increased shadow spread and a subtle 1px border in a lighter tint of the Primary color to denote focus.

Avoid heavy dark shadows; instead, use shadows tinted with the Deep Ocean Blue to maintain the ocean-themed atmosphere.

## Shapes

The design system uses a **Rounded** shape language to soften the industrial nature of maritime data. 
- Standard components (Buttons, Inputs) use a 0.5rem (8px) radius.
- Feature cards and Containers use a `rounded-lg` (16px) radius to create a friendly, modern container for complex charts.
- Selection indicators and Chips utilize a "Pill" shape to distinguish them from actionable buttons.

## Components

- **Cards:** The primary container. Must include a header area for titles and a footer for primary actions or metadata. Use plenty of internal padding (24px).
- **Buttons:** 
    - *Primary:* Deep Ocean Blue with White text.
    - *Secondary:* Seafoam Green outline with Seafoam Green text.
    - *Alert:* Coral background for destructive or urgent actions.
- **Data Chips:** Small, pill-shaped tags used on the map or in lists to show status (e.g., "Fuel: Low" or "Weather: Clear").
- **Map Markers:** High-contrast circular markers. Use a white outer ring and a colored inner core (Green/Yellow/Red) to ensure visibility against varied satellite imagery.
- **Input Fields:** Minimalist style with a subtle 1px border. On focus, the border transitions to Seafoam Green with a soft outer glow.
- **Alert Banners:** Full-width Coral banners at the top of the interface for critical weather or system warnings.