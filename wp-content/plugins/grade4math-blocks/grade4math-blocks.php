<?php
/**
 * Plugin Name: Grade 4 Math Blocks
 * Description: Custom Gutenberg blocks for the Grade 4 Math site
 * Version:     1.0.0
 * Author:      Claude
 */

function grade4math_blocks_init() {
    register_block_type( __DIR__ . '/build' );
}
add_action( 'init', 'grade4math_blocks_init' );
