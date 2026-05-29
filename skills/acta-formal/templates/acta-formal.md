# ACTA DE REUNION

**{{acta_number}}**

---

## I. Datos Generales

| Campo | Detalle |
|-------|---------|
| Fecha | {{date}} |
| Hora | {{start_time}} — {{end_time}} |
| Lugar | {{location}} |
| Tipo | {{meeting_type}} |
| Convocante | {{convener_name}} — {{convener_role}} |

## II. Lista de Asistencia y Quorum

| # | Nombre | Cargo | Asistencia | Firma |
|---|--------|-------|------------|-------|
{{#each attendees}}
| {{@index_plus_one}} | {{this.name}} | {{this.role}} | {{this.attendance}} | {{this.signature_status}} |
{{/each}}

**Quorum**: {{quorum_count}}/{{total_invited}} — {{quorum_status}}
**Fuente del quorum**: {{quorum_source}}

## III. Orden del Dia

{{#each agenda_items}}
{{@index_plus_one}}. {{this}}
{{/each}}

## IV. Desarrollo de la Sesion

{{development_content}}

## V. Acuerdos

| # | Acuerdo | Responsable | Fecha Limite | Estado |
|---|---------|-------------|--------------|--------|
{{#each agreements}}
| {{@index_plus_one}} | {{this.description}} | {{this.responsible}} | {{this.deadline}} | {{this.status}} |
{{/each}}

> Si el quorum no fue validado, registrar decisiones como pendientes o discusiones, no como acuerdos vinculantes.

## VI. Asuntos Varios y Pendientes

{{misc_content}}

## VII. Cierre

Se da por concluida la reunion a las **{{end_time}}**.
Proxima reunion programada: **{{next_meeting}}**

## VIII. Firmas

___________________________          ___________________________
{{president_name}}                   {{secretary_name}}
Presidente de la sesion              Secretario de actas

---

*Documento generado automaticamente — {{acta_number}}*
