import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        person = request.form["person"]
        field = request.form["field"]
        prompt = generate_prompt(person, field)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical writer."},
                # {"role": "user", "content": "Here are the facts that you should rely on when writing the biography: {}".format(facts)},
                {"role": "user", "content": prompt},
                # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                # {"role": "user", "content": "Where was it played?"}
            ],
            # prompt=generate_prompt(person, field),
            temperature=0.6,
        )
        # print(response)
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    print(result)
    return render_template("index.html", result=result)


def generate_prompt(person, field):
    return """Generate a biography for the following physician in the field of {}.

    The target audience for this are professionals in the medical writing field and pharmaceutical representatives.
    This bio should be written in a humble and professional tone, without exaggerating achievements.

    The biography should start with a summary paragraph. It should include their degrees, medical school, and where they currently work. Please include the number of years they
    have been practicing medicine, if any.
    The 2nd paragraph should be about any clinical trials that the person is a part of.
    The 3rd paragraph should be about any publications they have come up with.
    The 4th paragraph should be about any awards they have one.
    The 5th paragraph should be about any professional organizations they have attended.


Name: {}


Name: Wendy Verret
Wendy Verret is a renowned physician in the field of hepatocellular carcinoma (HCC). She completed her medical degree from the University of California, San Francisco (UCSF) and then pursued her residency in internal medicine at the same institution. She later went on to complete a fellowship in medical oncology at the University of Texas, MD Anderson Cancer Center. Dr. Verret's passion for HCC began during her fellowship training, where she witnessed the devastating impact of this disease on patients and their families. Since then, she has dedicated her career to advancing the field of HCC research and treatment. Dr. Verret has published numerous articles in peer-reviewed journals, including the Journal of Clinical Oncology and the Journal of Hepatology. Her research focuses on identifying novel therapeutic targets and developing new treatments for HCC. In addition to her research, Dr. Verret is also a dedicated clinician. She works closely with her patients to develop personalized treatment plans that take into account their unique medical history and preferences.

Publications
Wendy Verret has published 20 total publications, including the following highly-cited articles
- Atezolizumab plus Bevacizumab in Unresectable Hepatocellular Carcinoma, N Engl J Med
. 2020
- Patient-reported outcomes with atezolizumab plus bevacizumab versus sorafenib in patients with unresectable hepatocellular carcinoma (IMbrave150): an open-label, randomised, phase 3 trial, Lancet Oncol
. 2021
- IMbrave 151: a randomized phase II trial of atezolizumab combined with bevacizumab and chemotherapy in patients with advanced biliary tract cancer, Ther Adv Med Oncol
. 2021


Professional Organizations
Dr. Verret is a member of several professional organizations, including the American Society of Clinical Oncology and the International Liver Cancer Association.

Awards
She has also been recognized for her contributions to the field of HCC with numerous awards, including the Young Investigator Award from the American Association for the Study of Liver Diseases.

Clinical Trials
Dr. Verret has been involved in several notable clinical trials related to unresectable hepatocellular carcinoma. In a phase 1b trial, the combination of combination of atezolizumab and bevacizumab showed showed encouraging antitumor activity and safety.


Overall, Dr. Verret's commitment to improving the lives of patients with HCC has made her a respected leader in the field. Her research and clinical work continue to inspire others and bring hope to those affected by this devastating disease.
""".format(field,
        person.capitalize()
    )
