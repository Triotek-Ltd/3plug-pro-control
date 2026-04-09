import site from './site';
import group from './group';
import bench from './bench';
import server from './server';
import notification from './notification';
import accessRequests from './accessRequests';

let objects = {
	Site: site,
	Group: group,
	Bench: bench,
	Server: server,
	Notification: notification,
	AccessRequests: accessRequests,
};

export function getObject(name) {
	return objects[name];
}

export default objects;
