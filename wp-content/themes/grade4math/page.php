<?php get_header(); ?>

<section class="page-hero" style="background: linear-gradient(135deg, #4a90e2, #7b68ee);">
    <a href="<?php echo home_url('/'); ?>" class="back-link">← Back to Home</a>
    <h2><?php the_title(); ?></h2>
</section>

<div class="wp-page-wrap">
    <?php while ( have_posts() ) : the_post(); ?>
        <div class="wp-page-content">
            <?php the_content(); ?>
        </div>
    <?php endwhile; ?>
</div>

<?php get_footer(); ?>
