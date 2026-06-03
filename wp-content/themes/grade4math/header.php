<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>

<header id="site-header">
    <div class="logo">
        <span class="icon">🔢</span>
        <h1>
            <?php bloginfo('name'); ?>
            <span><?php bloginfo('description'); ?></span>
        </h1>
    </div>
    <nav>
        <ul>
            <li><a href="<?php echo home_url('/'); ?>">🏠 Home</a></li>
            <li><a href="<?php echo home_url('/?page=topic&topic=multiplication'); ?>">✖️ Multiply</a></li>
            <li><a href="<?php echo home_url('/?page=practice'); ?>">✏️ Practice</a></li>
            <li><a href="<?php echo home_url('/?page=quiz'); ?>">🏆 Quiz</a></li>
        </ul>
    </nav>
</header>
