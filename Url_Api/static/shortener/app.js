const form = document.getElementById('shortener-form');
const resultBox = document.getElementById('result-box');

if (form && resultBox) {
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const input = document.getElementById('long-url');
        const longUrl = input.value.trim();

        if (!longUrl) return;

        resultBox.style.display = 'block';
        resultBox.innerHTML = 'Creating your short link...';

        try {
            const response = await fetch('/shortener/create_urls/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.content || ''
                },
                body: JSON.stringify({ long_url: longUrl })
            });

            const data = await response.json();
            if (response.ok && data.short_url) {
                resultBox.innerHTML = `Your short link is: <a href="${data.short_url}" target="_blank" rel="noopener">${data.short_url}</a>`;
            } else {
                resultBox.innerHTML = 'Unable to create a short link right now.';
            }
        } catch (error) {
            resultBox.innerHTML = 'Something went wrong. Please try again.';
        }
    });
}
