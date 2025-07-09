{{- define "nginx-openshift.name" -}}
nginx
{{- end }}

{{- define "nginx-openshift.fullname" -}}
{{ include "nginx-openshift.name" . }}
{{- end }}
