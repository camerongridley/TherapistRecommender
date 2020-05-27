import pandas as pd

def categorize_credential(dirty_cred):
    # value: dirty entry, key: standardized entry
    cred_stubs = {
        'MFT' : 'LMFT',
        'family therapist' : 'LMFT',
        'Family Therapy' : 'LMFT',

        'LCSW' : 'LCSW',
        'social work' : 'LCSW',
        'LICSW' : 'LCSW',
        'LISW' : 'LCSW',

        'LPC':'LPC',
        'LCPC' : 'LPC',
        'Professional Clinical Counsel' : 'LPC',
        'professional counsel' : 'LPC',
        'Mental Health' : 'LPC',
        'LMHC' : 'LPC',
        'MHC' : 'LPC',
        'Psychotherapist' : 'LPC',

        'Psychologist' : 'Psychologist',
        'Psychoanalyst' : 'Psychologist',

        'LAC' : 'LAC',

    }
    # prep the string
    dirty_cred = dirty_cred.lower().strip()

    clean_cred = set()

    for k, v in cred_stubs.items():
        #print(f'is {k} in {dirty_cred}')
        #if dirty_cred.find(k) != -1:
        if k.lower().strip() in dirty_cred:
            print(f'Added {v} for {dirty_cred}')
            clean_cred.add(v)
    
    if len(clean_cred) == 1:
        return list(clean_cred)[0]
    elif len(clean_cred) > 1:
        return 'Multiple'
    else:
        return 'NA'

if __name__ == '__main__':
    sample = {'primary_credential':['AMFT',
    'AMFT - 101139',
    ' AMFT - 112025',
    ' AMFT - 113115',
    ' AMFT - #114002',
    ' AMFT - 117179',
    ' AMFT - 117386',
    ' AMFT - 117580',
    ' AMFT - 117600',
    ' AMFT - 86845',
    ' AMFT - 89543',
    ' AMFT - 95655',
    'Associate Clinical Social Worker',
    ' ASSOCIATE CLINICAL SOCIAL WORKER',
    ' Associate Counselor',
    ' Associate Marriage and Family Therapist',
    ' Associate Marriage and Family Therapist - 107773',
    ' Associate Marriage and Family Therapist - 108157',
    ' Associate Marriage and Family Therapist - 110372',
    ' Associate Marriage and Family Therapist - AMFT111314',
    'Clinical Psychologist',
    'Associate Marriage and Therapist',
    'Associate Marriage & Family Therapist',
    'ASSOCIATE MARRIAGE & FAMILY THERAPIST',
    'ASSOCIATE MARRIAGE & FAMILY THERAPIST - 95497',
    ' Associate Marriage & Family Therapist - IMF96641',
    ' Associate MFT - 99458',
    'Associate Professional Clinical Counselor',
    ' ASSOCIATE PROFESSIONAL CLINICAL COUNSELOR',
    'Associate Professional Clinical Counselor - 4851',
    ' Clinical Psychologist - 071009447',
    ' Clinical Psychologist - 071.009973',
    ' CLINICAL PSYCHOLOGIST - 071010142',
    ' Clinical Psychologist - 071-02662',
    ' Clinical Social Worker - 34005765A',
    ' Clinical Social Worker - 35945',
    ' Clinical Social Worker - 44SC04613000',
    ' Clinical Social Worker - 44SC05622300',
    'LAC',
    ' LAC - 37AC00352100',
    ' LAC - 37AC00419600',
    ' LAC, NCC',
    ' LAMFT',
    ' LCAT',
    ' LCAT - 000152',
    'LCAT - 000393',
    'LCAT - 5000705',
    'LCMFT',
    'LCMFT - LCM121'
    ]}
    # s = 'Clinical Social Worker - 35945'
    # print(s.lower().strip().find('social work'))

    df = pd.DataFrame(sample)
    df['new_cred'] = df['primary_credential'].map(categorize_credential)

    print(df)