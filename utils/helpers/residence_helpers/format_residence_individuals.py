def format_residence_individuals(individuals):
    return [
        {
            "individuo_id": i.DomicilioIndividuo.individuo_id,
            "nome": i.nome,
            "nome_social": i.nome_social,
            "data_nascimento": i.data_nascimento.isoformat() if i.data_nascimento else None,
            "cpf": i.cpf,
            "cns": i.cns,
            "celular": i.celular,
            "data_residencia": i.DomicilioIndividuo.data_residencia.isoformat() if i.DomicilioIndividuo.data_residencia else None,
            "mudou": i.DomicilioIndividuo.mudou,
            "renda_familia_salario_minimos": float(
                i.DomicilioIndividuo.renda_familia_salario_minimos) if i.DomicilioIndividuo.renda_familia_salario_minimos else None,
            "n_membros_familia": i.DomicilioIndividuo.n_membros_familia,
            "responsavel": i.DomicilioIndividuo.responsavel
        }
        for i in individuals
    ]
