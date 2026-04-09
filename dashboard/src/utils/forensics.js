function encodePathSegment(value) {
	return encodeURIComponent(String(value || ''));
}

export function getForensicDocumentRoute(documentType, documentName) {
	if (!documentType || !documentName) return null;

	const name = encodePathSegment(documentName);
	return {
		Site: `/sites/${name}`,
		Bench: `/benches/${name}`,
		Server: `/servers/${name}`,
		'Database Server': `/servers/${name}`,
		'Forensic Event': `/forensics/${name}`,
	}[documentType] || null;
}

export function getForensicJobRoute({ job, site, bench, server }) {
	if (!job) return null;

	const jobName = encodePathSegment(job);
	if (site) {
		return `/sites/${encodePathSegment(site)}/jobs/${jobName}`;
	}
	if (bench) {
		return `/benches/${encodePathSegment(bench)}/jobs/${jobName}`;
	}
	if (server) {
		return `/servers/${encodePathSegment(server)}/jobs/${jobName}`;
	}
	return null;
}

export function getDeskDocumentRoute(doctype, name) {
	if (!doctype || !name) return null;

	return `/app/${String(doctype).replace(/\s+/g, '-').toLowerCase()}/${encodePathSegment(name)}`;
}

export function getForensicPrimaryTargetLink(document) {
	if (!document) return null;

	const route = getForensicDocumentRoute(document.document_type, document.document_name);
	if (route) {
		return {
			label: document.document_name,
			route,
			external: false,
		};
	}

	const deskRoute = getDeskDocumentRoute(document.document_type, document.document_name);
	if (!deskRoute) return null;

	return {
		label: document.document_name,
		route: deskRoute,
		external: true,
	};
}

export function getForensicSourceLink(document) {
	if (!document?.source_doctype || !document?.source_name) return null;

	if (document.source_doctype === 'Agent Job') {
		const route = getForensicJobRoute(document);
		if (route) {
			return {
				label: document.source_name,
				route,
				external: false,
			};
		}
	}

	const route = getDeskDocumentRoute(document.source_doctype, document.source_name);
	if (!route) return null;

	return {
		label: document.source_name,
		route,
		external: true,
	};
}
