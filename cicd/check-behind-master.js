/**
 * Checks if branch is behind master.  If the branch is behind then an error is thrown.
 * This prevents overwriting or removing changes that have been committed to master.
 *
 * Usage:
 *
 * node check-behind-master.js $(git rev-list --left-right --count master...BRANCH_NAME) BRANCH_NAME
 */

const [behindCount, aheadCount, branchName] = process.argv.slice(2);

console.log(`${branchName} is behind master by ${behindCount} commit(s).`);
console.log(`${branchName} is ahead of master by ${aheadCount} commit(s).`);

if (behindCount > 0) {
    throw new Error(
        `Branch (${branchName}) is behind master by ${behindCount} commit(s).  ` +
        `Rebase your branch with "git pull --rebase origin master", resolving any conflicts, ` +
        `and force-pushing your branch back to remote with "git push -f origin ${branchName}".`)
}
