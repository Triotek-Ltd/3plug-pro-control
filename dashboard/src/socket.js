import { io } from 'socket.io-client';
import { getCachedResource, getCachedListResource } from 'frappe-ui';

function getSocketPort() {
	return (
		window.socketio_port ||
		import.meta.env.VITE_SOCKETIO_PORT ||
		window.location.port ||
		''
	);
}

export function initSocket() {
	let host = window.location.hostname;
	let siteName = window.site_name;
	let socketPort = getSocketPort();
	let port = socketPort ? `:${socketPort}` : '';
	let protocol = port ? 'http' : 'https';
	let url = `${protocol}://${host}${port}/${siteName}`;

	let socket = io(url, {
		withCredentials: true,
		reconnectionAttempts: 5,
	});

	socket.on('refetch_resource', (data) => {
		if (data.cache_key) {
			let resource =
				getCachedResource(data.cache_key) ||
				getCachedListResource(data.cache_key);
			if (resource) {
				resource.reload();
			}
		}
	});
	return socket;
}
