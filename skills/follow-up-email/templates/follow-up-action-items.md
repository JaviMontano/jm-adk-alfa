Subject: {{subject_prefix}}: {{meeting_title}}

# Follow-Up: {{meeting_title}}

Hola {{name}},

Gracias por participar en la reunion "{{meeting_title}}" del {{date}}.

## Tus Action Items

{{#each action_items}}
- [ ] **{{this.task}}**
  - Fecha limite: {{this.deadline}}
  - Contexto: {{this.context}}
{{/each}}

## Proximos Pasos

{{next_steps}}

Si tienes dudas sobre alguno de estos puntos, no dudes en responder a este correo.

{{signoff}},
{{sender_name}}
