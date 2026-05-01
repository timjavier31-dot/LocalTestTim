/* ============================================================
   Grade 4 Math – Question Banks
   ============================================================ */

const PRACTICE_BANK = {
    multiplication: [
        { level:'easy',   q:'What is 6 × 7?',                                                   a:'42' },
        { level:'easy',   q:'What is 9 × 4?',                                                   a:'36' },
        { level:'easy',   q:'What is 8 × 5?',                                                   a:'40' },
        { level:'easy',   q:'What is 3 × 12?',                                                  a:'36' },
        { level:'easy',   q:'What is 11 × 7?',                                                  a:'77' },
        { level:'easy',   q:'What is 6 × 6?',                                                   a:'36' },
        { level:'medium', q:'What is 12 × 9?',                                                  a:'108' },
        { level:'medium', q:'What is 23 × 4?',                                                  a:'92' },
        { level:'medium', q:'What is 15 × 6?',                                                  a:'90' },
        { level:'medium', q:'What is 14 × 7?',                                                  a:'98' },
        { level:'medium', q:'What is 18 × 5?',                                                  a:'90' },
        { level:'medium', q:'A box holds 12 crayons. How many crayons are in 8 boxes?',         a:'96 crayons' },
        { level:'hard',   q:'What is 24 × 13?',                                                 a:'312' },
        { level:'hard',   q:'What is 36 × 25?',                                                 a:'900' },
        { level:'hard',   q:'A store receives 45 boxes with 24 pens each. How many pens total?',a:'1,080 pens' },
        { level:'hard',   q:'What is 17 × 16?',                                                 a:'272' },
        { level:'hard',   q:'Each student needs 32 sheets of paper. There are 28 students. How many sheets?', a:'896 sheets' },
    ],
    division: [
        { level:'easy',   q:'What is 36 ÷ 4?',                                                  a:'9' },
        { level:'easy',   q:'What is 48 ÷ 6?',                                                  a:'8' },
        { level:'easy',   q:'What is 72 ÷ 8?',                                                  a:'9' },
        { level:'easy',   q:'What is 45 ÷ 5?',                                                  a:'9' },
        { level:'easy',   q:'What is 63 ÷ 7?',                                                  a:'9' },
        { level:'easy',   q:'What is 56 ÷ 8?',                                                  a:'7' },
        { level:'medium', q:'What is 84 ÷ 7?',                                                  a:'12' },
        { level:'medium', q:'What is 96 ÷ 8?',                                                  a:'12' },
        { level:'medium', q:'What is 108 ÷ 9?',                                                 a:'12' },
        { level:'medium', q:'132 students are split into groups of 11. How many groups?',       a:'12 groups' },
        { level:'medium', q:'What is 75 ÷ 5?',                                                  a:'15' },
        { level:'medium', q:'What is 91 ÷ 7?',                                                  a:'13' },
        { level:'hard',   q:'What is 156 ÷ 4?',                                                 a:'39' },
        { level:'hard',   q:'What is 252 ÷ 9?',                                                 a:'28' },
        { level:'hard',   q:'A teacher has 144 pencils shared equally among 12 students. How many each?', a:'12 pencils' },
        { level:'hard',   q:'What is 224 ÷ 8?',                                                 a:'28' },
        { level:'hard',   q:'248 apples are packed into bags of 8. How many bags?',             a:'31 bags' },
    ],
    fractions: [
        { level:'easy',   q:'Which is bigger: 1/2 or 1/4?',                                    a:'1/2' },
        { level:'easy',   q:'How many fourths make one whole?',                                 a:'4' },
        { level:'easy',   q:'What fraction of a dozen (12) is 3?',                             a:'1/4' },
        { level:'easy',   q:'Is 2/4 the same as 1/2?',                                         a:'Yes, they are equivalent' },
        { level:'easy',   q:'What fraction has a numerator of 2 and denominator of 5?',        a:'2/5' },
        { level:'medium', q:'Write an equivalent fraction for 1/2 with denominator 8.',        a:'4/8' },
        { level:'medium', q:'2/5 + 1/5 = ?',                                                   a:'3/5' },
        { level:'medium', q:'3/4 − 1/4 = ?',                                                   a:'2/4 or 1/2' },
        { level:'medium', q:'What is 3/6 simplified to its lowest terms?',                     a:'1/2' },
        { level:'medium', q:'5/8 + 2/8 = ?',                                                   a:'7/8' },
        { level:'medium', q:'Which is smaller: 2/3 or 3/5?',                                   a:'3/5 (10/15 vs 9/15 — so 3/5 is smaller)' },
        { level:'hard',   q:'Order from smallest to largest: 3/4, 1/2, 2/3.',                 a:'1/2, 2/3, 3/4' },
        { level:'hard',   q:'7/10 − 3/10 = ?',                                                 a:'4/10 or 2/5' },
        { level:'hard',   q:'Lisa ate 2/8 of a pizza and Tom ate 3/8. How much did they eat together?', a:'5/8' },
        { level:'hard',   q:'Write three fractions equivalent to 2/3.',                        a:'4/6, 6/9, 8/12 (or any correct answers)' },
    ],
    geometry: [
        { level:'easy',   q:'How many sides does a hexagon have?',                             a:'6' },
        { level:'easy',   q:'What do we call an angle that is exactly 90°?',                  a:'Right angle' },
        { level:'easy',   q:'How many lines of symmetry does a square have?',                 a:'4' },
        { level:'easy',   q:'What type of angle is 135°?',                                    a:'Obtuse angle' },
        { level:'easy',   q:'How many degrees are in a straight angle?',                      a:'180°' },
        { level:'medium', q:'What is the area of a rectangle 8 cm × 5 cm?',                  a:'40 cm²' },
        { level:'medium', q:'What is the perimeter of a square with side 9 cm?',             a:'36 cm' },
        { level:'medium', q:'What is the perimeter of a rectangle 12 cm × 7 cm?',           a:'38 cm' },
        { level:'medium', q:'A triangle has angles of 55° and 75°. What is the third angle?',a:'50°' },
        { level:'medium', q:'What is the name of a quadrilateral with 2 pairs of parallel sides?', a:'Parallelogram' },
        { level:'medium', q:'Name a shape with 5 sides.',                                     a:'Pentagon' },
        { level:'hard',   q:'What is the area of a triangle with base 10 cm and height 6 cm?', a:'30 cm²  (base × height ÷ 2)' },
        { level:'hard',   q:'A rectangle has an area of 72 cm² and a length of 9 cm. What is its width?', a:'8 cm' },
        { level:'hard',   q:'What is the perimeter of a regular hexagon with each side = 7 cm?', a:'42 cm' },
        { level:'hard',   q:'The area of a square is 49 cm². What is the length of one side?', a:'7 cm' },
    ],
    measurement: [
        { level:'easy',   q:'How many centimeters are in 1 meter?',                           a:'100 cm' },
        { level:'easy',   q:'How many minutes are in 1 hour?',                               a:'60 minutes' },
        { level:'easy',   q:'How many milliliters are in 1 liter?',                          a:'1,000 mL' },
        { level:'easy',   q:'How many months are in 2 years?',                               a:'24 months' },
        { level:'easy',   q:'How many grams are in 1 kilogram?',                             a:'1,000 g' },
        { level:'medium', q:'Convert 2.5 kg to grams.',                                      a:'2,500 g' },
        { level:'medium', q:'How many seconds are in 3 minutes?',                            a:'180 seconds' },
        { level:'medium', q:'A movie starts at 2:15 PM and ends at 4:45 PM. How long is the movie?', a:'2 hours 30 minutes' },
        { level:'medium', q:'Convert 350 cm to meters.',                                     a:'3.5 m' },
        { level:'medium', q:'A jug holds 750 mL. How many mL in 4 jugs?',                   a:'3,000 mL or 3 L' },
        { level:'medium', q:'How many days are in 5 weeks?',                                 a:'35 days' },
        { level:'hard',   q:'A book weighs 350 g. How much do 6 books weigh in kg?',        a:'2.1 kg (2,100 g)' },
        { level:'hard',   q:'John runs 1.5 km each day. How far does he run in 5 days?',    a:'7.5 km' },
        { level:'hard',   q:'School starts at 8:45 AM and ends at 3:15 PM. How long is the school day?', a:'6 hours 30 minutes' },
        { level:'hard',   q:'A tank holds 4.5 L. If 1,200 mL is used, how much is left in mL?', a:'3,300 mL' },
    ],
    data: [
        { level:'easy',   q:'A bar graph shows: Apples=5, Bananas=8, Oranges=3. Which fruit is most popular?', a:'Bananas' },
        { level:'easy',   q:'What type of graph uses pictures or symbols to show data?',     a:'Pictograph' },
        { level:'easy',   q:'The data set is: 4, 7, 2, 9, 7. What is the mode?',            a:'7 (appears most often)' },
        { level:'easy',   q:'What does the range tell us?',                                  a:'The difference between the highest and lowest values' },
        { level:'medium', q:'In a tally chart: |||| |||| | = how many?',                    a:'11' },
        { level:'medium', q:'Pictograph key: ⭐ = 5 books. If there are 7 stars, how many books?', a:'35 books' },
        { level:'medium', q:'Data: 12, 8, 15, 10, 5. What is the range?',                   a:'10 (15 − 5)' },
        { level:'medium', q:'Temperatures for 5 days: 22, 25, 19, 28, 21. What was the highest?', a:'28°C' },
        { level:'hard',   q:'10 students voted: 4 soccer, 3 basketball, 3 tennis. What fraction chose soccer?', a:'4/10 or 2/5' },
        { level:'hard',   q:'Data: 6, 8, 6, 9, 11. Find the mean (average).',              a:'8 (sum=40, 40÷5=8)' },
        { level:'hard',   q:'A bar graph scale shows each line = 4 units. A bar reaches 7 lines. What is the value?', a:'28' },
        { level:'hard',   q:'Data: 3, 5, 3, 7, 5, 3. Find the mode and range.',            a:'Mode = 3, Range = 4' },
    ],
};

const QUIZ_BANK = {
    multiplication: [
        { q:'What is 9 × 7?',                                                                 a:'63',  opts:['54','56','63','72'] },
        { q:'What is 12 × 8?',                                                                a:'96',  opts:['86','92','96','104'] },
        { q:'What is 6 × 11?',                                                               a:'66',  opts:['55','60','66','72'] },
        { q:'What is 4 × 15?',                                                               a:'60',  opts:['45','50','55','60'] },
        { q:'A bag has 7 apples. How many apples are in 9 bags?',                            a:'63',  opts:['54','63','72','81'] },
        { q:'What is 13 × 5?',                                                               a:'65',  opts:['50','55','60','65'] },
        { q:'A classroom has 6 rows of 9 desks. How many desks?',                           a:'54',  opts:['45','48','54','63'] },
        { q:'What is 8 × 12?',                                                               a:'96',  opts:['84','88','96','108'] },
        { q:'What property says 3 × 7 = 7 × 3?',                                           a:'Commutative', opts:['Associative','Commutative','Distributive','Zero'] },
        { q:'What is 11 × 11?',                                                              a:'121', opts:['110','115','121','132'] },
        { q:'What is 7 × 7?',                                                               a:'49',  opts:['42','49','56','63'] },
        { q:'24 students sit in 4 equal rows. How many in each row?',                       a:'6',   opts:['4','5','6','8'] },
    ],
    division: [
        { q:'What is 56 ÷ 7?',                                                               a:'8',  opts:['6','7','8','9'] },
        { q:'What is 72 ÷ 9?',                                                               a:'8',  opts:['7','8','9','10'] },
        { q:'45 cookies shared equally among 9 children. How many each?',                   a:'5',  opts:['4','5','6','7'] },
        { q:'What is 84 ÷ 4?',                                                               a:'21', opts:['18','20','21','24'] },
        { q:'What is 132 ÷ 11?',                                                             a:'12', opts:['10','11','12','13'] },
        { q:'Which of these is the QUOTIENT in 48 ÷ 6 = 8?',                               a:'8',  opts:['48','6','8','14'] },
        { q:'What is 96 ÷ 8?',                                                               a:'12', opts:['10','11','12','13'] },
        { q:'63 ÷ 9 = ?',                                                                    a:'7',  opts:['6','7','8','9'] },
        { q:'A bag holds 12 oranges. How many bags for 144 oranges?',                       a:'12', opts:['10','11','12','13'] },
        { q:'What is 100 ÷ 5?',                                                              a:'20', opts:['15','20','25','50'] },
        { q:'What is 144 ÷ 12?',                                                             a:'12', opts:['10','11','12','13'] },
        { q:'77 ÷ 7 = ?',                                                                    a:'11', opts:['7','9','11','13'] },
    ],
    fractions: [
        { q:'Which fraction is equivalent to 1/2?',                                          a:'2/4',  opts:['1/3','2/4','2/6','3/8'] },
        { q:'2/6 + 3/6 = ?',                                                                 a:'5/6',  opts:['5/12','5/6','6/6','1'] },
        { q:'Which fraction is the smallest?',                                               a:'1/4',  opts:['1/2','1/3','1/4','3/4'] },
        { q:'What is 3/4 − 1/4?',                                                           a:'2/4',  opts:['1/4','2/4','3/8','1/2'] },
        { q:'Which fraction equals 1 whole?',                                               a:'8/8',  opts:['4/8','6/8','7/8','8/8'] },
        { q:'Lisa ate 1/5 of a cake. What fraction is left?',                               a:'4/5',  opts:['1/5','2/5','3/5','4/5'] },
        { q:'Which is bigger: 3/4 or 2/3?',                                                 a:'3/4',  opts:['2/3','3/4','They are equal','Cannot tell'] },
        { q:'What is the denominator in the fraction 5/8?',                                 a:'8',    opts:['5','8','13','3'] },
        { q:'4/10 simplified is?',                                                           a:'2/5',  opts:['1/2','2/5','4/5','1/5'] },
        { q:'1/3 + 1/3 = ?',                                                                 a:'2/3',  opts:['1/3','2/3','2/6','1'] },
        { q:'Which fraction is between 1/4 and 3/4?',                                       a:'1/2',  opts:['1/8','1/2','7/8','1'] },
        { q:'How many eighths equal one half?',                                              a:'4',    opts:['2','3','4','6'] },
    ],
    geometry: [
        { q:'How many degrees are in a right angle?',                                        a:'90°',  opts:['45°','60°','90°','180°'] },
        { q:'A square has sides of 7 cm. What is its perimeter?',                           a:'28 cm', opts:['21 cm','28 cm','35 cm','49 cm'] },
        { q:'What shape has 5 sides?',                                                       a:'Pentagon', opts:['Hexagon','Pentagon','Octagon','Heptagon'] },
        { q:'Area of a rectangle 6 cm × 4 cm = ?',                                         a:'24 cm²', opts:['20 cm²','24 cm²','28 cm²','36 cm²'] },
        { q:'What type of angle is 47°?',                                                    a:'Acute', opts:['Right','Acute','Obtuse','Straight'] },
        { q:'A triangle has angles 60° and 70°. What is the third?',                       a:'50°',  opts:['40°','50°','60°','70°'] },
        { q:'How many sides does an octagon have?',                                          a:'8',    opts:['6','7','8','9'] },
        { q:'What is the area of a square with side 6 cm?',                                 a:'36 cm²', opts:['24 cm²','30 cm²','36 cm²','48 cm²'] },
        { q:'How many lines of symmetry does a rectangle have?',                            a:'2',    opts:['1','2','4','8'] },
        { q:'What do we call two lines that never meet?',                                   a:'Parallel lines', opts:['Intersecting lines','Perpendicular lines','Parallel lines','Diagonal lines'] },
        { q:'Perimeter of a rectangle 10 cm × 5 cm = ?',                                   a:'30 cm', opts:['15 cm','25 cm','30 cm','50 cm'] },
        { q:'What is the name of a triangle with all equal sides?',                         a:'Equilateral', opts:['Scalene','Isosceles','Equilateral','Right'] },
    ],
    measurement: [
        { q:'3 hours = how many minutes?',                                                   a:'180',  opts:['120','150','180','240'] },
        { q:'4,000 g = how many kg?',                                                        a:'4 kg', opts:['40 kg','4 kg','0.4 kg','400 kg'] },
        { q:'2.5 liters = how many mL?',                                                    a:'2,500 mL', opts:['250 mL','2,500 mL','25,000 mL','2,050 mL'] },
        { q:'How many cm are in 3 meters?',                                                  a:'300 cm', opts:['30 cm','300 cm','3,000 cm','30,000 cm'] },
        { q:'A class starts at 9:10 AM and ends at 10:45 AM. How long is the class?',      a:'1 h 35 min', opts:['1 h 25 min','1 h 30 min','1 h 35 min','1 h 45 min'] },
        { q:'Which unit would you use to measure the weight of a cat?',                     a:'kg',   opts:['mg','g','kg','tonnes'] },
        { q:'How many seconds are in 2 minutes?',                                            a:'120',  opts:['60','90','120','180'] },
        { q:'500 mL + 750 mL = ?',                                                           a:'1,250 mL', opts:['1,000 mL','1,250 mL','1,500 mL','1,750 mL'] },
        { q:'How many days are in a leap year?',                                             a:'366',  opts:['364','365','366','368'] },
        { q:'1 km = how many meters?',                                                       a:'1,000 m', opts:['100 m','500 m','1,000 m','10,000 m'] },
        { q:'A recipe needs 750 mL of milk. How many full liters is that?',                a:'0 full liters (less than 1 L)', opts:['0 full liters (less than 1 L)','1 liter','2 liters','3 liters'] },
        { q:'2 hours 20 min − 45 min = ?',                                                  a:'1 h 35 min', opts:['1 h 25 min','1 h 35 min','1 h 40 min','1 h 45 min'] },
    ],
    data: [
        { q:'A bar graph: Books=10, Comics=6, Magazines=4. How many more books than magazines?', a:'6', opts:['4','6','8','10'] },
        { q:'The mode of 3, 5, 3, 7, 5, 3 is?',                                            a:'3',   opts:['3','5','7','4.3'] },
        { q:'Pictograph: each 🍎 = 4. There are 5 symbols. How many apples?',              a:'20',  opts:['5','10','15','20'] },
        { q:'Data: 8, 12, 5, 9, 11. What is the range?',                                   a:'7',   opts:['5','7','9','12'] },
        { q:'Which graph is best for showing change over time?',                             a:'Line graph', opts:['Bar graph','Pictograph','Line graph','Tally chart'] },
        { q:'Tally marks: |||| |||| = ?',                                                   a:'10',  opts:['8','9','10','12'] },
        { q:'Data: 6, 8, 6, 9, 11. What is the mean?',                                     a:'8',   opts:['6','7','8','9'] },
        { q:'In a bar graph, the scale goes up by 5s. A bar is at the 7th line. What value?',a:'35', opts:['7','28','35','40'] },
        { q:'Which value appears most often: 4, 7, 2, 7, 9, 4, 7?',                       a:'7',   opts:['2','4','7','9'] },
        { q:'A survey: 5 prefer cats, 8 prefer dogs, 2 prefer fish. How many voted total?',a:'15',  opts:['10','13','15','17'] },
        { q:'What does a line plot use to show each data point?',                           a:'An X mark', opts:['A bar','A picture','An X mark','A circle'] },
        { q:'Data: 10, 20, 30, 40, 50. What is the mean?',                                 a:'30',  opts:['20','25','30','35'] },
    ],
};

/* ============================================================
   Utility
   ============================================================ */
function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function pick(arr, n) {
    return shuffle(arr).slice(0, n);
}

function getAllFromBank(bank) {
    return Object.values(bank).flat();
}

/* ============================================================
   PRACTICE
   ============================================================ */
function loadPractice() {
    const container = document.getElementById('practice-container');
    const filterTopic = document.getElementById('topic-filter') ? document.getElementById('topic-filter').value : 'all';
    const filterLevel = document.getElementById('level-filter') ? document.getElementById('level-filter').value : 'all';

    let pool = filterTopic === 'all' ? getAllFromBank(PRACTICE_BANK) : (PRACTICE_BANK[filterTopic] || []);
    if (filterLevel !== 'all') pool = pool.filter(p => p.level === filterLevel);
    if (pool.length === 0) { container.innerHTML = '<p style="text-align:center;color:#888;">No problems match that filter. Try a different combination!</p>'; return; }

    const problems = pick(pool, Math.min(6, pool.length));
    const levelColor = { easy: '#27ae60', medium: '#e67e22', hard: '#8e44ad' };
    const levelStars = { easy: '⭐', medium: '⭐⭐', hard: '⭐⭐⭐' };

    container.innerHTML = problems.map((p, i) => `
        <div class="problem-card ${p.level}">
            <div class="level">${levelStars[p.level]} ${p.level.charAt(0).toUpperCase() + p.level.slice(1)}</div>
            <div class="question">${p.q}</div>
            <button class="answer-btn" onclick="toggleAnswer(this)">Show Answer</button>
            <div class="answer">✅ Answer: ${p.a}</div>
        </div>
    `).join('');
}

function toggleAnswer(btn) {
    const answer = btn.nextElementSibling;
    const showing = answer.style.display === 'block';
    answer.style.display = showing ? 'none' : 'block';
    btn.textContent = showing ? 'Show Answer' : 'Hide Answer';
}

/* ============================================================
   QUIZ
   ============================================================ */
let quizQuestions = [];
let quizAnswers   = {};
let quizSubmitted = false;

function loadQuiz() {
    const filterTopic = document.getElementById('quiz-topic-filter') ? document.getElementById('quiz-topic-filter').value : 'all';
    let pool = filterTopic === 'all' ? getAllFromBank(QUIZ_BANK) : (QUIZ_BANK[filterTopic] || []);
    quizQuestions = pick(pool, Math.min(10, pool.length));
    quizAnswers   = {};
    quizSubmitted = false;

    const container = document.getElementById('quiz-container');
    const result    = document.getElementById('quiz-result');
    result.innerHTML = '';

    container.innerHTML = quizQuestions.map((q, i) => {
        const shuffledOpts = shuffle(q.opts);
        return `
        <div class="quiz-question" id="qq-${i}">
            <div class="q-number">Question ${i + 1}</div>
            <div class="q-text">${q.q}</div>
            <div class="q-options">
                ${shuffledOpts.map(opt => `
                <label class="q-option">
                    <input type="radio" name="q${i}" value="${opt}" onchange="recordAnswer(${i}, this.value)">
                    <span>${opt}</span>
                </label>`).join('')}
            </div>
        </div>`;
    }).join('');

    document.getElementById('quiz-submit').style.display = 'block';
    document.getElementById('quiz-retry').style.display = 'none';
}

function recordAnswer(index, value) {
    quizAnswers[index] = value;
}

function submitQuiz() {
    if (quizSubmitted) return;
    quizSubmitted = true;
    let score = 0;

    quizQuestions.forEach((q, i) => {
        const selected = quizAnswers[i];
        const isCorrect = selected === q.a;
        if (isCorrect) score++;

        const qEl = document.getElementById(`qq-${i}`);
        qEl.querySelectorAll('.q-option').forEach(label => {
            const input = label.querySelector('input');
            if (input.value === q.a) label.classList.add('correct');
            else if (input.value === selected && !isCorrect) label.classList.add('incorrect');
            input.disabled = true;
        });

        const note = document.createElement('div');
        note.className = 'q-result-note';
        note.textContent = isCorrect ? '✅ Correct!' : `❌ Correct answer: ${q.a}`;
        note.style.color = isCorrect ? '#27ae60' : '#e74c3c';
        qEl.appendChild(note);
    });

    const pct = Math.round((score / quizQuestions.length) * 100);
    const msg = pct === 100 ? '🏆 Perfect score! Outstanding!' :
                pct >= 80  ? '🌟 Great job! Almost perfect!' :
                pct >= 60  ? '👍 Good effort! Keep practicing!' :
                             '💪 Keep studying — you\'ll get there!';

    document.getElementById('quiz-result').innerHTML = `
        <div class="quiz-score">
            <div class="score-circle">${score}/${quizQuestions.length}</div>
            <div class="score-pct">${pct}%</div>
            <div class="score-msg">${msg}</div>
        </div>`;

    document.getElementById('quiz-submit').style.display = 'none';
    document.getElementById('quiz-retry').style.display = 'block';
    document.getElementById('quiz-result').scrollIntoView({ behavior: 'smooth' });
}

/* ============================================================
   Init
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('practice-container')) loadPractice();
    if (document.getElementById('quiz-container'))    loadQuiz();
});
