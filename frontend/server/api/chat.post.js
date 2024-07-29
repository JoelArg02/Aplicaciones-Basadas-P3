export default defineEventHandler(async (event) => {
	const config = useRuntimeConfig();
	const previosMessage = await readBody(event);

	// Añadir registros para depuración
	console.log('Received previosMessage:', previosMessage);

	if (!previosMessage.query || typeof previosMessage.query !== 'string') {
		console.error('Error: query is not valid');
		return {
			message: 'Error: query is not valid'
		};
	}

	const prompt = `User: ${previosMessage.query}\n`;

	console.log('Generated prompt:', prompt);

	try {
		const req = await fetch('http://localhost:3001/predict', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				query: prompt,
			})
		});

		const res = await req.json();
		console.log('res', res);

		if (res && res.response) {
			return {
				message: res.response.trim()
			};
		} else {
			throw new Error('Invalid response from API');
		}
	} catch (error) {
		console.error('Error fetching data from API:', error);
		return {
			message: 'Sorry, an error occurred while processing your request.'
		};
	}
});
