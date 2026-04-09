import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import frappeui from 'frappe-ui/vite';
import pluginRewriteAll from 'vite-plugin-rewrite-all';
import { sentryVitePlugin } from '@sentry/vite-plugin';
import dotenv from 'dotenv';
dotenv.config();

const sentryConfigured =
	Boolean(process.env.SENTRY_URL) &&
	Boolean(process.env.SENTRY_ORG) &&
	Boolean(process.env.SENTRY_PROJECT) &&
	Boolean(process.env.SENTRY_AUTH_TOKEN) &&
	process.env.DISABLE_SENTRY_PLUGIN !== '1';

const plugins = [
	frappeui({
		frappeProxy: true,
		lucideIcons: true,
		jinjaBootData: true,
		buildConfig: {
			outDir: '../press/public/dashboard',
			indexHtmlPath: '../press/www/dashboard.html',
			emptyOutDir: true,
			sourcemap: true,
		},
	}),
	vue(),
	vueJsx(),
	pluginRewriteAll(),
];

if (sentryConfigured) {
	plugins.push(
		sentryVitePlugin({
			url: process.env.SENTRY_URL,
			org: process.env.SENTRY_ORG,
			project: process.env.SENTRY_PROJECT,
			applicationKey: 'press-dashboard',
			authToken: process.env.SENTRY_AUTH_TOKEN,
			errorHandler: (err) => console.warn(err),
		}),
	);
}

export default defineConfig({
	plugins,
	server: {
		allowedHosts: true,
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src'),
		},
	},
	optimizeDeps: {
		include: [
			'feather-icons',
			'showdown',
			'highlight.js/lib/core',
			'interactjs',
		],
	},
	build: {
		chunkSizeWarningLimit: 2000,
	},
});
