from tensorflow.keras.models import load_model
import tensorflow as tf
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from openai import OpenAI

data="""Subfolder: acanthosis nigricans, Number of Images: 92
Subfolder: acne, Number of Images: 183
Subfolder: acne vulgaris, Number of Images: 335
Subfolder: acquired autoimmune bullous diseaseherpes gestationis, Number of Images: 67
Subfolder: acrodermatitis enteropathica, Number of Images: 92
Subfolder: actinic keratosis, Number of Images: 175
Subfolder: allergic contact dermatitis, Number of Images: 430
Subfolder: aplasia cutis, Number of Images: 72
Subfolder: basal cell carcinoma, Number of Images: 468
Subfolder: basal cell carcinoma morpheiform, Number of Images: 62
Subfolder: becker nevus, Number of Images: 63
Subfolder: behcets disease, Number of Images: 63
Subfolder: calcinosis cutis, Number of Images: 80
Subfolder: cheilitis, Number of Images: 106
Subfolder: congenital nevus, Number of Images: 68
Subfolder: dariers disease, Number of Images: 153
Subfolder: dermatofibroma, Number of Images: 79
Subfolder: dermatomyositis, Number of Images: 151
Subfolder: disseminated actinic porokeratosis, Number of Images: 60
Subfolder: drug eruption, Number of Images: 200
Subfolder: drug induced pigmentary changes, Number of Images: 71
Subfolder: dyshidrotic eczema, Number of Images: 83
Subfolder: eczema, Number of Images: 204
Subfolder: ehlers danlos syndrome, Number of Images: 127
Subfolder: epidermal nevus, Number of Images: 91
Subfolder: epidermolysis bullosa, Number of Images: 70
Subfolder: erythema annulare centrifigum, Number of Images: 88
Subfolder: erythema elevatum diutinum, Number of Images: 55
Subfolder: erythema multiforme, Number of Images: 236
Subfolder: erythema nodosum, Number of Images: 81
Subfolder: factitial dermatitis, Number of Images: 66
Subfolder: fixed eruptions, Number of Images: 125
Subfolder: folliculitis, Number of Images: 342
Subfolder: fordyce spots, Number of Images: 100
Subfolder: granuloma annulare, Number of Images: 211
Subfolder: granuloma pyogenic, Number of Images: 75
Subfolder: hailey hailey disease, Number of Images: 174
Subfolder: halo nevus, Number of Images: 82
Subfolder: hidradenitis, Number of Images: 90
Subfolder: ichthyosis vulgaris, Number of Images: 65
Subfolder: incontinentia pigmenti, Number of Images: 102
Subfolder: juvenile xanthogranuloma, Number of Images: 149
Subfolder: kaposi sarcoma, Number of Images: 156
Subfolder: keloid, Number of Images: 156
Subfolder: keratosis pilaris, Number of Images: 78
Subfolder: langerhans cell histiocytosis, Number of Images: 60
Subfolder: lentigo maligna, Number of Images: 83
Subfolder: lichen amyloidosis, Number of Images: 77
Subfolder: lichen planus, Number of Images: 491
Subfolder: lichen simplex, Number of Images: 97
Subfolder: livedo reticularis, Number of Images: 60
Subfolder: lupus erythematosus, Number of Images: 410
Subfolder: lupus subacute, Number of Images: 111
Subfolder: lyme disease, Number of Images: 129
Subfolder: lymphangioma, Number of Images: 100
Subfolder: malignant melanoma, Number of Images: 111
Subfolder: melanoma, Number of Images: 261
Subfolder: milia, Number of Images: 112
Subfolder: mucinosis, Number of Images: 92
Subfolder: mucous cyst, Number of Images: 79
Subfolder: mycosis fungoides, Number of Images: 182
Subfolder: myiasis, Number of Images: 67
Subfolder: naevus comedonicus, Number of Images: 73
Subfolder: necrobiosis lipoidica, Number of Images: 123
Subfolder: nematode infection, Number of Images: 260
Subfolder: neurodermatitis, Number of Images: 69
Subfolder: neurofibromatosis, Number of Images: 189
Subfolder: neurotic excoriations, Number of Images: 73
Subfolder: neutrophilic dermatoses, Number of Images: 361
Subfolder: nevocytic nevus, Number of Images: 86
Subfolder: nevus sebaceous of jadassohn, Number of Images: 95
Subfolder: papilomatosis confluentes and reticulate, Number of Images: 150
Subfolder: paronychia, Number of Images: 59
Subfolder: pediculosis lids, Number of Images: 151
Subfolder: perioral dermatitis, Number of Images: 61
Subfolder: photodermatoses, Number of Images: 348
Subfolder: pilar cyst, Number of Images: 93
Subfolder: pilomatricoma, Number of Images: 53
Subfolder: pityriasis lichenoides chronica, Number of Images: 73
Subfolder: pityriasis rosea, Number of Images: 193
Subfolder: pityriasis rubra pilaris, Number of Images: 278
Subfolder: porokeratosis actinic, Number of Images: 183
Subfolder: porokeratosis of mibelli, Number of Images: 78
Subfolder: porphyria, Number of Images: 127
Subfolder: port wine stain, Number of Images: 59
Subfolder: prurigo nodularis, Number of Images: 170
Subfolder: psoriasis, Number of Images: 653
Subfolder: pustular psoriasis, Number of Images: 53
Subfolder: pyogenic granuloma, Number of Images: 113
Subfolder: rhinophyma, Number of Images: 91
Subfolder: rosacea, Number of Images: 102
Subfolder: sarcoidosis, Number of Images: 349
Subfolder: scabies, Number of Images: 339
Subfolder: scleroderma, Number of Images: 309
Subfolder: scleromyxedema, Number of Images: 108
Subfolder: seborrheic dermatitis, Number of Images: 126
Subfolder: seborrheic keratosis, Number of Images: 69
Subfolder: solid cystic basal cell carcinoma, Number of Images: 66
Subfolder: squamous cell carcinoma, Number of Images: 581
Subfolder: stasis edema, Number of Images: 69
Subfolder: stevens johnson syndrome, Number of Images: 113
Subfolder: striae, Number of Images: 67
Subfolder: sun damaged skin, Number of Images: 66
Subfolder: superficial spreading melanoma ssm, Number of Images: 118
Subfolder: syringoma, Number of Images: 127
Subfolder: telangiectases, Number of Images: 126
Subfolder: tick bite, Number of Images: 73
Subfolder: tuberous sclerosis, Number of Images: 141
Subfolder: tungiasis, Number of Images: 152
Subfolder: urticaria, Number of Images: 151
Subfolder: urticaria pigmentosa, Number of Images: 112
Subfolder: vitiligo, Number of Images: 166
Subfolder: xanthomas, Number of Images: 53
Subfolder: xeroderma pigmentosum, Number of Images: 81"""
client=OpenAI(api_key='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')
def get_medical_advice_for_disease(user_input):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a medical chatbot that diagnoses diseases. User will input in the form: Disease: \"....\", Pulse Rate: \"...\", Oxygen level: \"....\", Temperature: \".....\" , you have to provide output in the form: Predicted disease: \"....\" , Treatment Plan: \"....\", Prescribed Drugs: \"....\", Specialization: \"....\". Prescribe safe drugs based on treatment plan. For specialization, if treatment plan involves visiting a doctor, it specifies which specialization of doctor to visit. Also some inputs from user may be unknown, diagnose and provide output with rest known inputs."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content

image_path = "edpBackend/out.jpg"
image = tf.io.read_file(image_path)
image = tf.io.decode_jpeg(image, channels=3)
image = tf.image.convert_image_dtype(image, tf.float32)
image = tf.image.resize(image, (224, 224))  # Resize the image as needed
image = tf.expand_dims(image, axis=0)
model2 = load_model('/home/yash/Downloads/v1.keras')
prediction = model2.predict(image)
prediction = prediction[0]
prediction = prediction.tolist()
subfolders=[]
for line in data.strip().split('\n'):
    # Split each line by comma and extract the subfolder name
    subfolder = line.split(':')[1].strip()
    subfolder=subfolder.split(',')[0]
    # Append the subfolder name to the list
    subfolders.append(subfolder)

###get max of prediction
max_index=0
for i in range(len(prediction)):
    if prediction[i]>prediction[max_index]:
        max_index=i

disease=subfolders[max_index]

user_input = f"Disease: \"{disease}\", Pulse Rate: \"80\", Oxygen level: \"90%\", Temperature: \"98.6\""
advice = get_medical_advice_for_disease(user_input)
print("Advice:", advice)
