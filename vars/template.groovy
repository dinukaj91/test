/**
 * Defines a pipeline template (as a sample with one job parameter 
 * that should be common for all pipelines)
 */
def call() {   
    freeStyleJob('pf-customer-notifications-build-pr-image') {
        description 'Build and push pf-customer-notifications docker image'
    }
}
