describe('Agenda de Contatos - CRUD', () => {
  const preencherFormulario = (nome, email, telefone) => {
    cy.get('input[type="text"]').first().clear().type(nome)
    cy.get('input[type="email"]').clear().type(email)
    cy.get('input[type="tel"]').clear().type(telefone)
  }

  const cardDoContato = (nome) =>
    cy
      .contains(nome)
      .parents()
      .filter(':has(.edit):has(.delete)')
      .first()

  beforeEach(() => {
    cy.visit('/')
  })

  it('deve incluir um novo contato', () => {
    const id = Date.now()
    const nome = `Contato Cypress ${id}`
    const email = `cypress${id}@teste.com`
    const telefone = '81999999999'

    preencherFormulario(nome, email, telefone)
    cy.get('.adicionar').click()

    cy.contains(nome).should('be.visible')
    cy.contains(email).should('be.visible')

    // Limpeza do dado criado para não poluir o ambiente compartilhado.
    cardDoContato(nome).within(() => {
      cy.get('.delete').click()
    })
    cy.contains(nome).should('not.exist')
  })

  it('deve alterar um contato existente', () => {
    const id = Date.now()
    const nomeOriginal = `Contato Editar ${id}`
    const nomeEditado = `Contato Alterado ${id}`
    const email = `editar${id}@teste.com`
    const telefone = '81988888888'

    preencherFormulario(nomeOriginal, email, telefone)
    cy.get('.adicionar').click()
    cy.contains(nomeOriginal).should('be.visible')

    cardDoContato(nomeOriginal).within(() => {
      cy.get('.edit').click()
    })

    cy.get('input[type="text"]').first().clear().type(nomeEditado)

    cy.get('body').then(($body) => {
      if ($body.find('.alterar').length) {
        cy.get('.alterar').click()
      } else if (
        $body
          .find('button')
          .filter((_, elemento) => /Salvar|Alterar/.test(elemento.innerText))
          .length
      ) {
        cy.contains('button', /Salvar|Alterar/).click()
      } else {
        cy.get('button[type="submit"]').first().click()
      }
    })

    cy.contains(nomeEditado).should('be.visible')
    cy.contains(nomeOriginal).should('not.exist')

    // Limpeza do dado criado.
    cardDoContato(nomeEditado).within(() => {
      cy.get('.delete').click()
    })
    cy.contains(nomeEditado).should('not.exist')
  })

  it('deve remover um contato', () => {
    const id = Date.now()
    const nome = `Contato Remover ${id}`
    const email = `remover${id}@teste.com`
    const telefone = '81977777777'

    preencherFormulario(nome, email, telefone)
    cy.get('.adicionar').click()
    cy.contains(nome).should('be.visible')

    cardDoContato(nome).within(() => {
      cy.get('.delete').click()
    })

    cy.contains(nome).should('not.exist')
  })
})
