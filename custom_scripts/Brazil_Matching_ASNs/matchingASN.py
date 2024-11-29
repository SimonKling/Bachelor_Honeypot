import pandas as pd

filenames = {
    './ASN_DDoS_Brazil/Azure_M_ASN.csv': 'Azure_M',
    './ASN_DDoS_Brazil/Azure_S_ASN.csv': 'Azure_S',
    './ASN_DDoS_Brazil/Google_M_ASN.csv': 'Google_M',
    './ASN_DDoS_Brazil/Google_S_ASN.csv': 'Google_S',
    './ASN_DDoS_Brazil/Oracle_M_ASN.csv': 'Oracle_M',
    './ASN_DDoS_Brazil/Oracle_S_ASN.csv': 'Oracle_S',
    './ASN_DDoS_Brazil/Digital_M_ASN.csv': 'DigitalOcean_M',
    './ASN_DDoS_Brazil/Digital_S_ASN.csv': 'DigitalOcean_S',
}

def find_asn_overlaps(filenames):
    asn_to_files = {}
    file_to_asns = {}

    for file, identifier in filenames.items():
        df = pd.read_csv(file, usecols=['ASN'], low_memory=True)
        df['ASN'] = df['ASN'].astype(str)
        asns = set(df['ASN'].unique())
        file_to_asns[identifier] = asns
        for asn in asns:
            asn_to_files.setdefault(asn, set()).add(identifier)

    overlapping_all = {asn: identifiers for asn, identifiers in asn_to_files.items() if len(identifiers) > 7}

    provider_groups = {
        'Azure': ['Azure_M', 'Azure_S'],
        'Google': ['Google_M', 'Google_S'],
        'Oracle': ['Oracle_M', 'Oracle_S'],
        'DigitalOcean': ['DigitalOcean_M', 'DigitalOcean_S'],
    }

    provider_to_asns = {}
    for provider, identifiers in provider_groups.items():
        provider_asns = set()
        for identifier in identifiers:
            provider_asns.update(file_to_asns[identifier])
        provider_to_asns[provider] = provider_asns
        
        
    gcp_azure_overlap_asns = provider_to_asns['Google'].intersection(provider_to_asns['Azure'])
    
    
    gcp_azure_overlap = {
    asn: identifiers.intersection({'Google_M', 'Google_S', 'Azure_M', 'Azure_S'})
    for asn, identifiers in asn_to_files.items()
    if asn in gcp_azure_overlap_asns
}

    all_providers_overlap_asns = set.intersection(*provider_to_asns.values())
    all_providers_overlap = {asn: asn_to_files[asn] for asn in all_providers_overlap_asns}

    return overlapping_all, gcp_azure_overlap, all_providers_overlap

if __name__ == "__main__":
    overlapping_all, gcp_azure_overlap, all_providers_overlap = find_asn_overlaps(filenames)

    overlapping_all_df = pd.DataFrame([
        {'ASN': asn, 'Identifiers': ', '.join(sorted(identifiers))}
        for asn, identifiers in overlapping_all.items()
    ])
    overlapping_all_df.to_csv('./overlapping_asns_all_instances.csv', index=False)

    gcp_azure_overlap_df = pd.DataFrame([
        {'ASN': asn, 'Identifiers': ', '.join(sorted(identifiers)) }
        for asn, identifiers in gcp_azure_overlap.items()
    ])
    gcp_azure_overlap_df.to_csv('./overlapping_asns_gcp_azure.csv', index=False)

    all_providers_overlap_df = pd.DataFrame([
        {'ASN': asn, 'Identifiers': ', '.join(sorted(identifiers))}
        for asn, identifiers in all_providers_overlap.items()
    ])
    all_providers_overlap_df.to_csv('./overlapping_asns_all_providers.csv', index=False)
