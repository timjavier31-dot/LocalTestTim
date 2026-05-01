<?php
$base      = home_url( '/' );
$pre_topic = isset( $_GET['topic'] ) ? sanitize_key( $_GET['topic'] ) : 'all';
$valid     = [ 'multiplication', 'division', 'fractions', 'geometry', 'measurement', 'data' ];
if ( ! in_array( $pre_topic, $valid ) ) $pre_topic = 'all';
?>

<section class="page-hero" style="background: linear-gradient(135deg, #f093fb, #f5576c);">
    <a href="<?php echo home_url('/'); ?>" class="back-link">← Back to Home</a>
    <h2>🏆 Math Quiz</h2>
    <p>10 random multiple-choice questions — try to get a perfect score!</p>
</section>

<section class="quiz-section">
    <div class="filter-bar">
        <div class="filter-group">
            <label for="quiz-topic-filter">📚 Topic:</label>
            <select id="quiz-topic-filter" onchange="loadQuiz()">
                <option value="all" <?php echo $pre_topic === 'all' ? 'selected' : ''; ?>>All Topics</option>
                <option value="multiplication" <?php echo $pre_topic === 'multiplication' ? 'selected' : ''; ?>>✖️ Multiplication</option>
                <option value="division"       <?php echo $pre_topic === 'division'       ? 'selected' : ''; ?>>➗ Division</option>
                <option value="fractions"      <?php echo $pre_topic === 'fractions'      ? 'selected' : ''; ?>>½ Fractions</option>
                <option value="geometry"       <?php echo $pre_topic === 'geometry'       ? 'selected' : ''; ?>>📐 Geometry</option>
                <option value="measurement"    <?php echo $pre_topic === 'measurement'    ? 'selected' : ''; ?>>📏 Measurement</option>
                <option value="data"           <?php echo $pre_topic === 'data'           ? 'selected' : ''; ?>>📊 Data & Graphs</option>
            </select>
        </div>
        <button class="refresh-btn" onclick="loadQuiz()">🔄 New Quiz</button>
    </div>

    <div id="quiz-container"></div>

    <div class="quiz-actions">
        <button id="quiz-submit" class="submit-btn" onclick="submitQuiz()" style="display:none;">Submit Answers 🏁</button>
        <button id="quiz-retry"  class="retry-btn"  onclick="loadQuiz()"   style="display:none;">Try Again 🔄</button>
    </div>

    <div id="quiz-result"></div>
</section>
