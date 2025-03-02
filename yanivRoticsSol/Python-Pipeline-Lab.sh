// Define a reusable function to run a stage with a command
//this script worked in my jenkins
def runStage = { stageName, command ->
    stage(stageName) {
        echo "Starting stage: ${stageName}"
        sh command
    }
}

// Define a function for parallel steps (Lint and Security Test)
def parallelSteps = {
    parallel (
        'Lint': {
            runStage('Lint', 'echo "Running Python linting (e.g., flake8)..."')
        },
        'Security Test': {
            runStage('Security Test', 'echo "Running security checks (e.g., safety)..."')
        }
    )
}

node {
    // Clone Stage: Mock cloning from GitHub
    runStage('Clone', 'echo "Cloning repository..."')

    // Build Stage: Mock building the Python project
    runStage('Build', 'echo "Building Python project..."')

    // Parallel Tasks: Run Lint and Security Test in parallel
    stage('Parallel Tasks') {
        parallelSteps()
    }

    // Optional Deploy Stage: User input to decide on deployment
    stage('Deploy') {
        // Use input step to ask user if deployment should proceed
        def proceedDeploy = input message: 'Deploy to production?', parameters: [booleanParam(defaultValue: false, description: 'Proceed with deployment?', name: 'DEPLOY')]
        if (proceedDeploy) {
            runStage('Deploy', 'echo "Deploying Python project to production..."')
        } else {
            echo "Deployment skipped."
        }
    }

    // Cleanup Stage: Post actions to clean up workspace
    stage('Cleanup') {
        runStage('Cleanup', 'echo "Cleaning up workspace..."')
    }
}
