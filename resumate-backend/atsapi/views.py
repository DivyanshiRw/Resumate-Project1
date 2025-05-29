from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pdfplumber
import docx
import traceback

from .resumate_scorer import compute_resume_score  # import the scorer

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def analyze_resume(request):
    resume_file = request.FILES.get('resume')
    job_desc = request.data.get('jobdesc', '')

    if not resume_file:
        return Response({'error': 'No resume file provided'}, status=400)

    # Extract text based on file type
    if resume_file.name.endswith('.pdf'):
        with pdfplumber.open(resume_file) as pdf:
            text = ''.join([page.extract_text() or '' for page in pdf.pages])
    elif resume_file.name.endswith('.docx'):
        doc = docx.Document(resume_file)
        text = ' '.join([para.text for para in doc.paragraphs])
    else:
        return Response({'error': 'Unsupported file type'}, status=400)

    try:
        # Call scoring logic
        result = compute_resume_score(text, job_desc)

        return Response({
            'resume_text': text[:500],  # Optional: preview text
            'score': result['score'],
            'quality': result.get('quality', ''),              
            'suggestions': result.get('suggestions', []),
            'breakdown': result['breakdown'],
            'details': result['details'],
            'message': 'Resume analyzed successfully!'
        })

    except Exception as e:
        print("🔴 Exception occurred in analyze_resume view:")
        print(traceback.format_exc())  # <-- this will show full traceback in terminal

        return Response({
            'error': str(e),
            'trace': traceback.format_exc()  # <-- this will also return it in API response
        }, status=500)