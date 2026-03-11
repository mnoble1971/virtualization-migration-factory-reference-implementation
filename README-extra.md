######
open-admin user:

at cmdline
# htpasswd -c -B -b /tmp/user.htpasswd open-admin "some password"
# oc create secret generic htpass-secret --from-file=htpasswd=/tmp/user.htpasswd -n openshift-config

enable compoentent "htpasswd-configuration"
