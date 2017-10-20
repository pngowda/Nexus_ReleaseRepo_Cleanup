node('master') {
	def pythonCleanupScript     = '/Nexus_Repo_Cleanup.py'
	def buildWrapper  = './code/vms/gradlew'
	withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'id_nex',
    usernameVariable: 'nexusUsername', passwordVariable: 'nexusPassword']])
	{
		stage ('checkout'){ 
			checkout scm
		}
		stage ('cleanup nexus'){
			echo "Building on branch: ${env.BRANCH_NAME}"
			if(isUnix()) {
				sh "chmod +x ${pythonCleanupScript}"
				sh "python ${pythonCleanupScript}"
			}
			else{
				bat "python ${pythonCleanupScript}"
			}
		}
	}
}
