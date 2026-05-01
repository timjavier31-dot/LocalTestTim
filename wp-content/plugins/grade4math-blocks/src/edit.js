import { __ } from '@wordpress/i18n';
import { useBlockProps, InspectorControls, RichText } from '@wordpress/block-editor';
import { PanelBody, SelectControl, TextControl } from '@wordpress/components';

const LEVELS = [
    { label: '⭐ Easy',          value: 'easy'   },
    { label: '⭐⭐ Medium',      value: 'medium' },
    { label: '⭐⭐⭐ Challenge', value: 'hard'   },
];

const TOPICS = [
    { label: '✖️ Multiplication', value: 'multiplication' },
    { label: '➗ Division',       value: 'division'       },
    { label: '½ Fractions',       value: 'fractions'      },
    { label: '📐 Geometry',       value: 'geometry'       },
    { label: '📏 Measurement',    value: 'measurement'    },
    { label: '📊 Data & Graphs',  value: 'data'           },
];

export default function Edit( { attributes, setAttributes } ) {
    const { question, answer, hint, level, topic, studentAnswer } = attributes;

    const blockProps = useBlockProps( {
        className: `math-problem-block level-${ level }`,
    } );

    const levelLabel = LEVELS.find( l => l.value === level )?.label ?? level;
    const topicLabel = TOPICS.find( t => t.value === topic )?.label ?? topic;

    return (
        <>
            <InspectorControls>
                <PanelBody title="Problem Settings" initialOpen={ true }>
                    <SelectControl
                        label="Difficulty Level"
                        value={ level }
                        options={ LEVELS }
                        onChange={ val => setAttributes( { level: val } ) }
                    />
                    <SelectControl
                        label="Topic"
                        value={ topic }
                        options={ TOPICS }
                        onChange={ val => setAttributes( { topic: val } ) }
                    />
                    <TextControl
                        label="Hint (optional)"
                        value={ hint }
                        onChange={ val => setAttributes( { hint: val } ) }
                        placeholder="Add an optional hint…"
                    />
                </PanelBody>
            </InspectorControls>

            <div { ...blockProps }>
                <div className="mp-badge">
                    <span className="mp-level">{ levelLabel }</span>
                    <span className="mp-sep">·</span>
                    <span className="mp-topic">{ topicLabel }</span>
                </div>

                <RichText
                    tagName="div"
                    className="mp-question"
                    value={ question }
                    onChange={ val => setAttributes( { question: val } ) }
                    placeholder="Type your math question here…"
                />

                { hint && (
                    <div className="mp-hint">💡 Hint: { hint }</div>
                ) }

                <div className="mp-student-answer-editor">
                    <div className="mp-student-answer-label">✏️ Student Answer Line</div>
                    <RichText
                        tagName="div"
                        className="mp-student-answer-preview"
                        value={ studentAnswer }
                        onChange={ val => setAttributes( { studentAnswer: val } ) }
                        placeholder="Optional: pre-fill a sample answer or leave blank for students to fill in…"
                    />
                    <p className="mp-editor-note">👆 Shows as a writeable input on the live site.</p>
                </div>

                <div className="mp-answer-editor">
                    <div className="mp-answer-label">✅ Correct Answer (hidden)</div>
                    <RichText
                        tagName="div"
                        className="mp-answer-text"
                        value={ answer }
                        onChange={ val => setAttributes( { answer: val } ) }
                        placeholder="Type the correct answer here…"
                    />
                </div>

                <p className="mp-editor-note">👆 Correct answer will be hidden with a Show/Hide button on the live site.</p>
            </div>
        </>
    );
}
