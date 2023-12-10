document.getElementById('codeForm').addEventListener('submit', async function(e) {
    e.preventDefault();


    const code = document.getElementById('codeInput').value;
    try {
        var challenge_name = document.getElementById("title").innerHTML;
        console.log(challenge_name);
        challenge_name = challenge_name.replace(/🐍 | 🐍/g, '').replace(' ', '_').toLowerCase();
        console.log(challenge_name);
        
        const response = await fetch('/execute/' + challenge_name, {
            method: 'POST',
            body: new FormData(this)
        });
        const data = await response.json();

        var output_container = document.getElementById("output-container");
        var outputs = output_container.childElementCount;

        document.getElementById('output1').innerHTML = '<strong class="output-label">Output 1:</strong> ' + data[0];
        if (outputs >= 2) {
            document.getElementById('output2').innerHTML = '<strong class="output-label">Output 2:</strong> ' + data[1];
            console.log(2);
        }
        if (outputs >= 3) {
            document.getElementById('output3').innerHTML = '<strong class="output-label">Output 3:</strong> ' + data[2];
        }
        if (outputs == 4) {
            document.getElementById('output4').innerHTML = '<strong class="output-label">Output 4:</strong> ' + data[3];
            console.log(4);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
