{{/*
Generate the name of the chart.
*/}}
{{- define "flask-app.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{/*
Generate the full name for resources.
*/}}
{{- define "flask-app.fullname" -}}
{{- printf "%s-%s" (include "flask-app.name" .) .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
