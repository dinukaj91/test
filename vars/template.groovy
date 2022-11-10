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
                                        $class: 'GroovyScript',
                                        script: [
                                            classpath: [], 
                                            sandbox: false, 
                                            script: 
                                                "return['Could not get The environemnts']"
                                        ]
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
