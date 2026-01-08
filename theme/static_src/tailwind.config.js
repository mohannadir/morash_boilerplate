/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */
        
        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        '../../**/*.py'
    ],
    theme: {
        screens: {
            'xxs': '320px', // Added 'xxs' screen size
            'xs': '480px', // Added 'xs' screen size
            'sm': '640px',
            'md': '768px',
            'lg': '1024px',
            'xl': '1280px',
        },
        extend: {
            colors: {
                'default' : {
                    'DEFAULT': '#11181C',
                },
                'primary' : {
                    'DEFAULT': '#4b64e7',
                    'light' : '#e1eafd',
                },
                'secondary' : {
                    'DEFAULT' : '#090e15',
                },
                'card' : {
                    'DEFAULT': '#141826',
                },
                'success' : {
                    'DEFAULT': '#22c55e',
                    'light': '#dcfce7',
                    'dark' : '#14532d',
                },
                'warning' : {
                    'DEFAULT': '#f97316',
                    'light' : '#ffedd5',
                    'dark' : '#7c2d12',
                },
                'error' : {
                    'DEFAULT': '#ef4444',
                    'light' : '#fee2e2',
                    'dark' : '#7f1d1d',
                }
            }
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
