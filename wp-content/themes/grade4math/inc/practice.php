<?php
$base       = home_url( '/' );
$pre_topic  = isset( $_GET['topic'] ) ? sanitize_key( $_GET['topic'] ) : 'all';
$valid      = [ 'multiplication', 'division', 'fractions', 'geometry', 'measurement', 'data' ];
if ( ! in_array( $pre_topic, $valid ) ) $pre_topic = 'all';
?>

<section class="page-hero" style="background: linear-gradient(135deg, #4a90e2, #7b68ee);">
    <a href="<?php echo home_url('/'); ?>" class="back-link">← Back to Home</a>
    <h2>✏️ Practice Problems</h2>
    <p>New random problems every time — click "New Problems" to get a fresh set!</p>
</section>

<section class="practice-section">
    <div class="filter-bar">
        <div class="filter-group">
            <label for="topic-filter">📚 Topic:</label>
            <select id="topic-filter" onchange="loadPractice()">
                <option value="all" <?php echo $pre_topic === 'all' ? 'selected' : ''; ?>>All Topics</option>
                <option value="multiplication" <?php echo $pre_topic === 'multiplication' ? 'selected' : ''; ?>>✖️ Multiplication</option>
                <option value="division"       <?php echo $pre_topic === 'division'       ? 'selected' : ''; ?>>➗ Division</option>
                <option value="fractions"      <?php echo $pre_topic === 'fractions'      ? 'selected' : ''; ?>>½ Fractions</option>
                <option value="geometry"       <?php echo $pre_topic === 'geometry'       ? 'selected' : ''; ?>>📐 Geometry</option>
                <option value="measurement"    <?php echo $pre_topic === 'measurement'    ? 'selected' : ''; ?>>📏 Measurement</option>
                <option value="data"           <?php echo $pre_topic === 'data'           ? 'selected' : ''; ?>>📊 Data & Graphs</option>
            </select>
        </div>
        <div class="filter-group">
            <label for="level-filter">⭐ Level:</label>
            <select id="level-filter" onchange="loadPractice()">
                <option value="all">All Levels</option>
                <option value="easy">⭐ Easy</option>
                <option value="medium">⭐⭐ Medium</option>
                <option value="hard">⭐⭐⭐ Challenge</option>
            </select>
        </div>
        <button class="refresh-btn" onclick="loadPractice()">🔄 New Problems</button>
    </div>

    <div class="problems-grid" id="practice-container">
        <p style="text-align:center; color:#888;">Loading problems...</p>
    </div>
</section>
