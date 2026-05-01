<?php
$base  = home_url( '/' );
$topic = sanitize_key( $_GET['topic'] ?? '' );

$topics = [
    'multiplication' => [
        'icon'  => '✖️',
        'color' => '#4a90e2',
        'label' => 'Multiplication',
        'intro' => 'Multiplication is a fast way to add the same number many times. When you know your times tables, you can solve problems quickly and easily!',
        'pages' => [
            [ 'label' => '⭐ Easy Level', 'url' => 'http://testsite.local/easy-level/', 'color' => '#27ae60' ],
        ],
        'concepts' => [
            [ 'title' => 'Times Tables (1–12)', 'body' => 'A times table shows what you get when you multiply a number by 1 through 12. Example: 7 × 1 = 7, 7 × 2 = 14, 7 × 3 = 21 ... 7 × 12 = 84' ],
            [ 'title' => 'Arrays', 'body' => 'An array is a group of objects arranged in rows and columns. 3 rows × 4 columns = 12 objects total.' ],
            [ 'title' => '2-Digit × 1-Digit', 'body' => 'To multiply 23 × 4: multiply the ones (3 × 4 = 12, write 2 carry 1), then the tens (2 × 4 = 8, plus 1 = 9). Answer: 92.' ],
            [ 'title' => 'Multiplication Properties', 'body' => 'Commutative: 4 × 7 = 7 × 4. Associative: (2 × 3) × 4 = 2 × (3 × 4). Zero property: any number × 0 = 0.' ],
        ],
        'examples' => [
            '6 × 9 = 54',
            '12 × 7 = 84',
            '25 × 4 = 100',
            '3 bags with 8 apples each = 3 × 8 = 24 apples',
        ],
        'tip' => 'To multiply by 9, multiply by 10 then subtract the number! Example: 9 × 7 = 70 − 7 = 63 🎯',
    ],
    'division' => [
        'icon'  => '➗',
        'color' => '#27ae60',
        'label' => 'Division',
        'intro' => 'Division is the process of splitting a number into equal groups. It is the opposite of multiplication — knowing your times tables makes division much easier!',
        'concepts' => [
            [ 'title' => 'What is Division?', 'body' => 'Division means sharing equally. 20 ÷ 4 = 5 means: 20 items split into 4 equal groups gives 5 in each group.' ],
            [ 'title' => 'Fact Families', 'body' => 'Multiplication and division are linked. If 6 × 8 = 48, then 48 ÷ 6 = 8 and 48 ÷ 8 = 6. These four facts are a fact family.' ],
            [ 'title' => 'Long Division', 'body' => 'Steps: Divide → Multiply → Subtract → Bring down. Example: 96 ÷ 4. How many times does 4 go into 9? → 2. 2 × 4 = 8. 9 − 8 = 1. Bring down 6 → 16 ÷ 4 = 4. Answer: 24.' ],
            [ 'title' => 'Remainders', 'body' => 'Sometimes a number does not divide evenly. 17 ÷ 5 = 3 remainder 2 (written as 3 R2). The remainder is always smaller than the divisor.' ],
        ],
        'examples' => [
            '72 ÷ 8 = 9',
            '84 ÷ 7 = 12',
            '156 ÷ 4 = 39',
            '25 ÷ 4 = 6 R1',
        ],
        'tip' => 'To check your division answer, multiply it back! If 84 ÷ 7 = 12, check: 12 × 7 = 84 ✅',
    ],
    'fractions' => [
        'icon'  => '½',
        'color' => '#e67e22',
        'label' => 'Fractions',
        'intro' => 'A fraction represents a part of a whole. The top number (numerator) tells how many parts we have, and the bottom number (denominator) tells how many equal parts the whole is divided into.',
        'concepts' => [
            [ 'title' => 'Numerator & Denominator', 'body' => 'In the fraction 3/4: the numerator is 3 (parts we have) and the denominator is 4 (total equal parts). Read as "three quarters."' ],
            [ 'title' => 'Equivalent Fractions', 'body' => 'Fractions that look different but are equal in value. 1/2 = 2/4 = 3/6 = 4/8. Multiply or divide the numerator and denominator by the same number.' ],
            [ 'title' => 'Comparing Fractions', 'body' => 'Same denominator: compare numerators (3/8 > 2/8). Different denominators: find a common denominator first. 1/2 vs 1/3 → 3/6 vs 2/6 → 1/2 is bigger.' ],
            [ 'title' => 'Adding & Subtracting Fractions', 'body' => 'With the same denominator: just add or subtract the numerators. 2/5 + 1/5 = 3/5. 4/7 − 2/7 = 2/7. The denominator stays the same!' ],
        ],
        'examples' => [
            '1/4 + 2/4 = 3/4',
            '5/8 − 2/8 = 3/8',
            '2/3 is equivalent to 4/6',
            '3/4 > 2/3 because 9/12 > 8/12',
        ],
        'tip' => 'Think of fractions as pizza slices! The denominator is how many slices total, the numerator is how many you have. 🍕',
    ],
    'geometry' => [
        'icon'  => '📐',
        'color' => '#8e44ad',
        'label' => 'Geometry',
        'intro' => 'Geometry is the study of shapes, sizes, and the properties of figures and spaces. In Grade 4, we explore 2D shapes, angles, lines, and how to find area and perimeter.',
        'concepts' => [
            [ 'title' => '2D Shapes & Polygons', 'body' => 'Triangle (3 sides), Quadrilateral (4 sides), Pentagon (5), Hexagon (6), Octagon (8). Special quadrilaterals: Square, Rectangle, Parallelogram, Rhombus, Trapezoid.' ],
            [ 'title' => 'Types of Angles', 'body' => 'Right angle = exactly 90°. Acute angle = less than 90°. Obtuse angle = more than 90° but less than 180°. Straight angle = 180°.' ],
            [ 'title' => 'Area', 'body' => 'Area = the space inside a shape. Rectangle: Area = length × width. Example: 8 cm × 5 cm = 40 cm². Triangle: Area = (base × height) ÷ 2.' ],
            [ 'title' => 'Perimeter', 'body' => 'Perimeter = the total distance around a shape. Add all the sides together. Rectangle: P = 2 × (length + width). Square: P = 4 × side.' ],
        ],
        'examples' => [
            'Area of 9 × 6 rectangle = 54 cm²',
            'Perimeter of square with side 7 cm = 28 cm',
            'A triangle with angles 50° and 60° has a third angle of 70°',
            'A square has 4 lines of symmetry',
        ],
        'tip' => 'Remember: Area is measured in square units (cm²) and Perimeter is measured in regular units (cm). 📏',
    ],
    'measurement' => [
        'icon'  => '📏',
        'color' => '#e74c3c',
        'label' => 'Measurement',
        'intro' => 'Measurement helps us describe the world around us — how long, how heavy, how much liquid, and what time it is. We use different units for different types of measurements.',
        'concepts' => [
            [ 'title' => 'Length', 'body' => 'Metric: 10 mm = 1 cm, 100 cm = 1 m, 1000 m = 1 km. Imperial: 12 inches = 1 foot, 3 feet = 1 yard. Use cm/m for everyday objects, km for distances.' ],
            [ 'title' => 'Mass / Weight', 'body' => '1000 grams (g) = 1 kilogram (kg). A paper clip weighs about 1 g. A bag of sugar weighs about 1 kg. Use grams for light items, kilograms for heavier ones.' ],
            [ 'title' => 'Volume / Capacity', 'body' => '1000 millilitres (mL) = 1 litre (L). A teaspoon ≈ 5 mL. A water bottle ≈ 500 mL. A large jug ≈ 1 L or more.' ],
            [ 'title' => 'Time', 'body' => '60 seconds = 1 minute. 60 minutes = 1 hour. 24 hours = 1 day. 7 days = 1 week. 365 days = 1 year. Elapsed time = end time − start time.' ],
        ],
        'examples' => [
            '2.5 km = 2,500 m',
            '3,500 g = 3.5 kg',
            '2 hours 15 minutes = 135 minutes',
            'A movie from 1:30 PM to 3:45 PM lasts 2 h 15 min',
        ],
        'tip' => 'For elapsed time, count the hours first, then the minutes. Start → End. 🕐',
    ],
    'data' => [
        'icon'  => '📊',
        'color' => '#16a085',
        'label' => 'Data & Graphs',
        'intro' => 'Data is information we collect and organize. Graphs help us see patterns and compare information quickly. In Grade 4, we read and create several types of graphs.',
        'concepts' => [
            [ 'title' => 'Bar Graphs', 'body' => 'Bar graphs use bars of different heights to compare categories. The taller the bar, the larger the value. Always read the scale carefully — each line may represent more than 1 unit.' ],
            [ 'title' => 'Pictographs', 'body' => 'Pictographs use pictures or symbols to represent data. Each symbol represents a certain number (shown in the key). Count the symbols and multiply by the key value.' ],
            [ 'title' => 'Line Plots', 'body' => 'Line plots show data on a number line with X marks. Each X = one piece of data. Great for showing how often values occur (frequency).' ],
            [ 'title' => 'Mean, Mode, Range', 'body' => 'Mode = the most common value. Range = largest − smallest. Mean (average) = sum of all values ÷ number of values. Example: 4, 7, 7, 9 → Mode=7, Range=5, Mean=6.75.' ],
        ],
        'examples' => [
            'Bar graph: Apples=12, Bananas=8 → Apples are more popular',
            'Pictograph key: 🍎 = 4 fruits. 5 symbols = 20 fruits',
            'Data: 3, 5, 5, 7, 10 → Mode=5, Range=7',
            'Temperatures: 22, 24, 19, 27, 23 → Range = 8°C',
        ],
        'tip' => 'When reading a bar graph, always check the scale on the side — it shows what each unit represents! 👀',
    ],
];

$t = $topics[ $topic ] ?? null;
if ( ! $t ) {
    wp_redirect( home_url( '/' ) );
    exit;
}
?>

<section class="topic-hero" style="background: linear-gradient(135deg, <?php echo $t['color']; ?>, <?php echo $t['color']; ?>aa);">
    <a href="<?php echo home_url('/'); ?>" class="back-link">← Back to Home</a>
    <div class="topic-hero-icon"><?php echo $t['icon']; ?></div>
    <h2><?php echo $t['label']; ?></h2>
    <p><?php echo $t['intro']; ?></p>
</section>

<section class="topic-content">
    <div class="topic-inner">

        <div class="concepts-grid">
            <?php foreach ( $t['concepts'] as $i => $c ) : ?>
            <div class="concept-card">
                <div class="concept-num"><?php echo $i + 1; ?></div>
                <h3><?php echo $c['title']; ?></h3>
                <p><?php echo $c['body']; ?></p>
            </div>
            <?php endforeach; ?>
        </div>

        <div class="examples-box">
            <h3>📝 Examples</h3>
            <ul>
                <?php foreach ( $t['examples'] as $ex ) : ?>
                <li><?php echo $ex; ?></li>
                <?php endforeach; ?>
            </ul>
        </div>

        <div class="tip-box">
            <span class="tip-label">💡 Pro Tip</span>
            <p><?php echo $t['tip']; ?></p>
        </div>

        <?php if ( ! empty( $t['pages'] ) ) : ?>
        <div class="topic-pages">
            <h3>📄 Lesson Pages</h3>
            <div class="topic-pages-list">
                <?php foreach ( $t['pages'] as $p ) : ?>
                <a href="<?php echo esc_url( $p['url'] ); ?>"
                   class="topic-page-link"
                   style="border-color:<?php echo esc_attr( $p['color'] ); ?>; color:<?php echo esc_attr( $p['color'] ); ?>;">
                    <?php echo esc_html( $p['label'] ); ?> →
                </a>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endif; ?>

        <div class="topic-actions">
            <a href="<?php echo esc_url( home_url( '/?page=practice&topic=' . $topic ) ); ?>" class="action-btn practice-btn">✏️ Practice <?php echo $t['label']; ?></a>
            <a href="<?php echo esc_url( home_url( '/?page=quiz&topic=' . $topic ) ); ?>" class="action-btn quiz-btn">🏆 Quiz on <?php echo $t['label']; ?></a>
        </div>

    </div>
</section>
