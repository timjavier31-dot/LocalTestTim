import { useBlockProps, RichText } from '@wordpress/block-editor';

const LEVEL_LABELS = {
    easy:   '⭐ Easy',
    medium: '⭐⭐ Medium',
    hard:   '⭐⭐⭐ Challenge',
};

const TOPIC_LABELS = {
    multiplication: '✖️ Multiplication',
    division:       '➗ Division',
    fractions:      '½ Fractions',
    geometry:       '📐 Geometry',
    measurement:    '📏 Measurement',
    data:           '📊 Data & Graphs',
};

export default function save( { attributes } ) {
    const { question, answer, hint, level, topic, studentAnswer } = attributes;

    const blockProps = useBlockProps.save( {
        className: `math-problem-block level-${ level }`,
    } );

    return (
        <div { ...blockProps }>
            <div className="mp-badge">
                <span className="mp-level">{ LEVEL_LABELS[ level ] }</span>
                <span className="mp-sep">·</span>
                <span className="mp-topic">{ TOPIC_LABELS[ topic ] }</span>
            </div>

            <RichText.Content tagName="div" className="mp-question" value={ question } />

            { hint && (
                <div className="mp-hint">💡 Hint: { hint }</div>
            ) }

            <div className="mp-student-answer-wrap">
                <label className="mp-student-answer-label">✏️ Your Answer:</label>
                <input
                    type="text"
                    className="mp-student-answer-input"
                    defaultValue={ studentAnswer || '' }
                    placeholder="Write your answer here…"
                />
            </div>

            <details className="mp-details">
                <summary className="mp-show-btn">Show Answer</summary>
                <div className="mp-answer-reveal">
                    ✅ <RichText.Content tagName="span" value={ answer } />
                </div>
            </details>
        </div>
    );
}
