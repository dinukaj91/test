/**
 * Defines a pipeline template (as a sample with one job parameter 
 * that should be common for all pipelines)
 */
def call() {   
    freeStyleJob() {
        description 'Build and push pf-customer-notifications docker image'
    }
}
