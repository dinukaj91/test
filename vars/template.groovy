/**
 * Defines a pipeline template (as a sample with one job parameter 
 * that should be common for all pipelines)
 */

properties([
    parameters([
        [$class: 'CascadeChoiceParameter', 
            choiceType: 'PT_SINGLE_SELECT',
            description: 'Select a choice',
            filterLength: 1,
            filterable: true,
            name: 'choice1',
            script: [$class: 'GroovyScript',
                fallbackScript: [
                    classpath: [], 
                    sandbox: true, 
                    script: 'return ["ERROR"]'
                ],
                script: [
                    classpath: [], 
                    sandbox: true, 
                    script: """
                        if (ENVIRONMENT == 'lab') { 
                            return['aaa','bbb']
                        }
                        else {
                            return['ccc', 'ddd']
                        }
                    """.stripIndent()
                ]
            ]
        ]
    ])
])

def call() {   
    pipeline {
        agent { label 'ap-slave-ecs' }
        parameters {
            string(name: 'myInput', description: 'Some pipeline parameters')
        }
        stages {
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
