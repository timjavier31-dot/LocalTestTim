import { registerBlockType } from '@wordpress/blocks';
import { useBlockProps, RichText } from '@wordpress/block-editor';
import metadata from './block.json';
import Edit from './edit';
import save from './save';
import './style.css';

/* Handles blocks saved before the studentAnswer field was added */
const deprecated = [
    {
        attributes: {
            question: { type: 'string', default: '' },
            answer:   { type: 'string', default: '' },
            hint:     { type: 'string', default: '' },
            level:    { type: 'string', default: 'easy' },
            topic:    { type: 'string', default: 'multiplication' },
        },
        save( { attributes } ) {
            const LEVEL_LABELS = { easy: '⭐ Easy', medium: '⭐⭐ Medium', hard: '⭐⭐⭐ Challenge' };
            const TOPIC_LABELS = { multiplication: '✖️ Multiplication', division: '➗ Division', fractions: '½ Fractions', geometry: '📐 Geometry', measurement: '📏 Measurement', data: '📊 Data & Graphs' };
            const { question, answer, hint, level, topic } = attributes;
            const blockProps = useBlockProps.save( { className: `math-problem-block level-${ level }` } );
            return (
                <div { ...blockProps }>
                    <div className="mp-badge">
                        <span className="mp-level">{ LEVEL_LABELS[ level ] }</span>
                        <span className="mp-sep">·</span>
                        <span className="mp-topic">{ TOPIC_LABELS[ topic ] }</span>
                    </div>
                    <RichText.Content tagName="div" className="mp-question" value={ question } />
                    { hint && <div className="mp-hint">💡 Hint: { hint }</div> }
                    <details className="mp-details">
                        <summary className="mp-show-btn">Show Answer</summary>
                        <div className="mp-answer-reveal">
                            ✅ <RichText.Content tagName="span" value={ answer } />
                        </div>
                    </details>
                </div>
            );
        },
    },
];

registerBlockType( metadata.name, { edit: Edit, save, deprecated } );
