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
                script: [
                    classpath: [], 
                    sandbox: false, 
                    script: """
                            return['ccc', 'ddd']
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
            string(name: 'myInput', description: 'Some pipeline parameterssssssss')
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
