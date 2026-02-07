async function main() {
  const MatchRegistry = await ethers.getContractFactory("MatchRegistry");
  const contract = await MatchRegistry.deploy();

  await contract.deployed();

  console.log("MatchRegistry deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
