
cat <<EOF > quay_authority.json
{
  "username":"$QUAY_ID",
  "password":"$QUAY_PASSWORD"  
}
EOF

oc get secret/pull-secret -n openshift-config -ojson | \
jq -r '.data[".dockerconfigjson"]' | \
base64 -d - | \
jq '.[]."quay.io/johnibm" += input' - quay_authority.json > temp_config.json

#oc set data secret/pull-secret -n openshift-config --from-file=.dockerconfigjson=jm_registry_auths.json
oc set data secret/pull-secret -n openshift-config --from-file=.dockerconfigjson=temp_config.json
oc get secret/pull-secret -n openshift-config -ojson | jq -r '.data[".dockerconfigjson"]' | base64 -d -


