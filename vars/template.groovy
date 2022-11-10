/**
 * Defines a pipeline template (as a sample with one job parameter 
 * that should be common for all pipelines)
 */



def call() {   
    pipeline {
        agent { label 'ap-slave-ecs' }
        stages {
            stage('Parameters'){
                steps {
                    script {
                    properties([
                            parameters([
                                [$class: 'ChoiceParameter', 
                                    choiceType: 'PT_SINGLE_SELECT', 
                                    description: 'Select the Environemnt from the Dropdown List', 
                                    filterLength: 1, 
                                    filterable: false, 
                                    name: 'Env', 
                                    script: [
                                        import jenkins.model.*
                                        import hudson.model.*
                                        import groovy.json.JsonSlurper

                                        if (branch.trim()) {
                                            credentialsId = 'bbfe5765-9add-4d2c-b10f-9b8c16b8cd19'
                                            def gitHubToken = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
                                                 com.cloudbees.plugins.credentials.common.StandardUsernameCredentials.class,
                                                    Jenkins.instance,
                                                    null,
                                                    null
                                            ).find{it.id == credentialsId};

                                            def urlConnect = new URL("https://api.github.com/repos/Propertyfinder/"+repoName+"/commits?sha="+branch+"&per_page=10")
                                            def connection = urlConnect.openConnection()
                                            connection.setRequestProperty("Authorization", "token "+gitHubToken.password)

                                            def result = new JsonSlurper().parseText(connection.content.text)

                                            def commits = []

                                            for (i = 0; i <result.size; i++) {
                                                commits.add(result[i]['sha'].take(10))
                                            }
                                            return commits
                                        }
                                    ]
                                ]
                            ])
                        ])
                    }
                }
            }
            stage('Stage one') {
                steps {
                    script {
                        echo "Parameter from template creation: "
                    }
                }
            }
            stage('Stage two') {
                steps {
                    script {
                        echo "Job input parameter: "
                    }
                }
            }
        }
    }
}
