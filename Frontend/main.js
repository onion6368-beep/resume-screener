const resume = document.getElementById("resume-file");
const jobDescription = document.getElementById("job-description");
const analyseBtn = document.getElementById("analyse-btn");
const resultsection = document.getElementById("result-section")


resume.addEventListener("change", () => {
    const file = resume.files[0];
    if(file){
        document.querySelector(".upload-text").textContent = file.name;
        document.querySelector(".upload-box span").textContent = '';
    }
});

analyseBtn.addEventListener("click", function() {

    const file = resume.files[0];

    const description = jobDescription.value;

    const formdata = new FormData();

    formdata.append("file",file);

    formdata.append("job_description",description)

    fetch("http://127.0.0.1:8000/upload",{
        method: "POST",
        body:formdata
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.score-num').textContent = data.match_score;
        document.querySelector('.score-info h2').textContent = data.hiring_recommendation;
        document.querySelector('.score-info p').textContent = data.match_summary;

        document.getElementById('s-tags').innerHTML = data.strengths
        .map(s=>`<span class="green-bubble">${s}</span>`).join('');

        document.getElementById('w-tags').innerHTML = data.missing_skills
        .map(s=>`<span class="red-bubble">${s}</span>`).join('');

        document.querySelector('.summary-section p').textContent = data.summary;

        document.querySelector('.upload-box').style.pointerEvents = 'none';
        document.querySelector('.upload-box').style.opacity = '0.5';
        analyseBtn.disabled = true;
        analyseBtn.textContent = '✓ Analysed';

        document.getElementById('result-section').style.display = 'flex';
    })
})
