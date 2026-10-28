template = """
Your job is to look at two data points. 
You receive a core-entry and a comparison-entry.
You also receive a similarity score.
Determin if the similarity score, which can be 
inaccurate. You must look at the entrys and 
decide if the similarity score assigned is plausible or 
not.
#################Input start#####################
Core-entry:
    label: {comparison_label}
    description: {core_description}
    entity_type: {entity_type}

Comparison-entry:
    comparison entry: {comparison_data}

Similarity score: {score}
##############Input end####################
Return True if the similarity score is accurate,
return False if the similarity score does not match
the semantic similarity of the entrys.
Also submit a str giving a reason for your decision.
############Outout format#######################
{
similarity: boolean,
reasoning: str
}
#################################################

"""