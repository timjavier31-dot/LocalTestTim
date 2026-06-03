<?php
$base = home_url( '/' );
$topics = [
    [ 'slug' => 'multiplication', 'icon' => '✖️',  'label' => 'Multiplication', 'color' => 'blue',   'desc' => 'Master times tables up to 12×12 and multi-digit multiplication.' ],
    [ 'slug' => 'division',       'icon' => '➗',  'label' => 'Division',       'color' => 'green',  'desc' => 'Learn long division and how it relates to multiplication.' ],
    [ 'slug' => 'fractions',      'icon' => '½',   'label' => 'Fractions',      'color' => 'orange', 'desc' => 'Understand parts of a whole, comparing and ordering fractions.' ],
    [ 'slug' => 'geometry',       'icon' => '📐',  'label' => 'Geometry',       'color' => 'purple', 'desc' => 'Explore shapes, angles, lines, and symmetry.' ],
    [ 'slug' => 'measurement',    'icon' => '📏',  'label' => 'Measurement',    'color' => 'red',    'desc' => 'Work with length, weight, volume, and time.' ],
    [ 'slug' => 'data',           'icon' => '📊',  'label' => 'Data & Graphs',  'color' => 'teal',   'desc' => 'Read and create bar graphs, line plots, and tables.' ],
];
?>

<section class="hero">
    <h2>Welcome to Grade 4 Math! 🎉</h2>
    <p>Learn, practice, and master math skills with fun lessons and exercises designed just for you!</p>
    <div class="badges">
        <span class="badge">📐 Geometry</span>
        <span class="badge">✖️ Multiplication</span>
        <span class="badge">➗ Division</span>
        <span class="badge">½ Fractions</span>
        <span class="badge">📏 Measurement</span>
    </div>
    <div style="margin-top:25px; display:flex; gap:15px; justify-content:center; flex-wrap:wrap;">
        <a href="<?php echo esc_url( $base . '?page=practice' ); ?>" class="hero-btn">✏️ Practice Problems</a>
        <a href="<?php echo esc_url( $base . '?page=quiz' ); ?>" class="hero-btn hero-btn-alt">🏆 Take a Quiz</a>
    </div>
</section>

<section class="topics-section">
    <h2>📖 Math Topics</h2>
    <p class="subtitle">Click a topic to start learning!</p>
    <div class="topics-grid">
        <?php foreach ( $topics as $t ) : ?>
        <a href="<?php echo esc_url( $base . '?page=topic&topic=' . $t['slug'] ); ?>" class="topic-card <?php echo $t['color']; ?>">
            <span class="emoji"><?php echo $t['icon']; ?></span>
            <h3><?php echo $t['label']; ?></h3>
            <p><?php echo $t['desc']; ?></p>
        </a>
        <?php endforeach; ?>
    </div>
</section>

<section class="funfacts">
    <h2>🏆 Math Fun Facts</h2>
    <div class="facts-grid">
        <div class="fact-box"><span class="number">144</span><span class="label">= 12 × 12<br>The biggest times table!</span></div>
        <div class="fact-box"><span class="number">360°</span><span class="label">in a full circle</span></div>
        <div class="fact-box"><span class="number">1,000</span><span class="label">ones = 1 thousand</span></div>
        <div class="fact-box"><span class="number">3.14</span><span class="label">Pi — the magic circle number!</span></div>
    </div>
</section>
