node('windows ') {
	def pythonCleanupScript     = "Nexus_Repo_Cleanup\\Nexus_Repo_Cleanup.exe"
	def buildWrapper  = './code/vms/gradlew'
	withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'nex_id',
    usernameVariable: 'nexusUsername', passwordVariable: 'nexusPassword']])
	{
		stage ('checkout'){ 
			checkout scm
		}
		stage ('cleanup nexus'){
			echo "Building on branch: ${env.BRANCH_NAME}"
			if(isUnix()) {
				sh "chmod +x ${pythonCleanupScript}"
				sh "${env.WORKSPACE}\\${pythonCleanupScript} siemens_esd com.lmsintl.accent requirements"
			}
			else{
				bat "${env.WORKSPACE}\\${pythonCleanupScript} siemens_esd com.lmsintl.accent requirements"
			}
		}
	}
}
