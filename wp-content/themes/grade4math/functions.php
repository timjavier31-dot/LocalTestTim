<?php
function grade4math_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    register_nav_menus( [ 'primary' => 'Primary Menu' ] );
}
add_action( 'after_setup_theme', 'grade4math_setup' );

function grade4math_enqueue() {
    wp_enqueue_style(  'grade4math-style',  get_stylesheet_uri() );
    wp_enqueue_script( 'grade4math-script', get_template_directory_uri() . '/js/grade4math.js', [], '1.0', true );
}
add_action( 'wp_enqueue_scripts', 'grade4math_enqueue' );
