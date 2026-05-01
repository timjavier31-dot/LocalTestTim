# Grade 4 Math — WordPress Site

A custom WordPress site built as an interactive math learning platform for Grade 4 students.

## Features

- **6 Math Topics** — Multiplication, Division, Fractions, Geometry, Measurement, Data & Graphs
- **Random Practice Problems** — 90+ problems across all topics, filtered by topic and difficulty
- **Random Quiz** — 10 multiple-choice questions per session with scoring
- **Custom Gutenberg Block** — "Math Problem" block for teachers to add styled problems anywhere
- **Fully custom theme** — built from scratch with PHP, CSS, and JavaScript

## Project Structure

```
wp-content/
├── themes/
│   └── grade4math/          # Custom WordPress theme
│       ├── style.css         # Theme styles
│       ├── functions.php     # Theme setup
│       ├── index.php         # Main router
│       ├── page.php          # WordPress page template
│       ├── header.php
│       ├── footer.php
│       ├── inc/
│       │   ├── home.php      # Homepage
│       │   ├── topic.php     # Topic lesson pages
│       │   ├── practice.php  # Random practice problems
│       │   └── quiz.php      # Random quiz
│       └── js/
│           └── grade4math.js # Question banks + quiz logic
│
└── plugins/
    └── grade4math-blocks/    # Custom Gutenberg block plugin
        ├── grade4math-blocks.php
        ├── src/
        │   ├── block.json    # Block metadata
        │   ├── index.js      # Block registration
        │   ├── edit.js       # Editor component (React)
        │   ├── save.js       # Frontend output
        │   └── style.css     # Block styles
        └── build/            # Compiled output (wp-scripts)
```

## Tech Stack

- **WordPress** (PHP)
- **Custom Theme** — PHP, CSS, vanilla JavaScript
- **Custom Gutenberg Block** — React, @wordpress/scripts
- **Local development** — LocalWP

## Setup Instructions

1. Install [LocalWP](https://localwp.com/) and create a new site
2. Clone this repo into `wp-content/` inside your site's `app/public/` folder
3. In WP Admin → Appearance → Themes → Activate **Grade 4 Math**
4. In WP Admin → Plugins → Activate **Grade 4 Math Blocks**
5. Build the block plugin:
   ```bash
   cd plugins/grade4math-blocks
   npm install
   npm run build
   ```
6. Visit your local site

## Screenshots

> Add screenshots here after deployment
