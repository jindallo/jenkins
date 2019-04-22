import pytest
import logging
import os
import errno
import shutil
from configparser import ConfigParser
from tools.adtools.modules.uds import uds
from tools.adtools.modules.util.asimov_bundle import AsimovBundle
from tools.adtools.modules.asimov.s32v import S32V
from tools.adtools.modules.asimov.asimov_constants import (SecurityLevel)
from tools.adtools.libs.uds_manager.uds_client_manager import UDSClientManager
from uds_manager.uds_client_manager import UDSClientTransportType
from tools.adtools.libs.asimov_managers.asimov_uds_client import AsimovUDSClientManager

CFG_PATH = os.path.abspath(os.path.dirname(__file__)) + "/pytest.ini"

class Test():
    def test_read_calibration(self):
        print("[Jin]")
        assert 1==1

    @pytest.fixture(scope="class")
    def asimov_bundle(self):
        self._asimov_bundle = AsimovBundle()
        return self._asimov_bundle

    @pytest.fixture(scope="class")
    def s32v(self):
        self._s32v = S32V()
        return self._s32v


    @pytest.fixture(scope="session", autouse=True)
    def logger(self):
        logger = logging.getLogger(os.path.basename(__file__))
        logger.setLevel(logging.DEBUG)
        return logger


    @pytest.fixture(scope="class")
    def download_bundle(self, asimov_bundle):
        # Get configuration file (assume default file)
        cfg = ConfigParser()
        assert cfg.read(CFG_PATH)

        # Parse configuration file
        path = cfg.get("master", "local_path")

        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                return False

        # Get latest master bundle
        print("\nDownloading latest master bundle")
        assert asimov_bundle.get_latest_master_bundle(path)
        # Return local path
        yield path
        shutil.rmtree(path)


    @pytest.fixture(scope="class")
    def uds_client_mgr(self, s32v):
        # Make sure we can ping Asimov
        assert s32v.ping(timeout=30)
        # Create UDS client
        udscm = AsimovUDSClientManager(s32v, UDSClientTransportType.DoIP, debug=True)
        # Return UDS client object
        yield udscm
        # Teardown
        udscm.disconnect()



    def _get_tar_from_bundle(self, bundle_path):
        """Return the tar file in the bundle
        Args:
            bundle_path (str) : Path to bundle
        Returns:
            str : path to tar file if it exists (None otherwise)
        """
        dirlist = os.listdir(bundle_path)
        for f in dirlist:
            if ".tar.gz" in f:
                return bundle_path + "/" + f
        return None



    def test_flash(self, logger, uds_client_mgr):
        print("[Jin] test_flash")
        udsc = uds_client_mgr
        # Get configuration file (assume default file)
        cfg = ConfigParser()
        assert cfg.read(CFG_PATH)

        # Parse configuration file
        bundle_path = cfg.get("master", "local_path")
        print("[Jin]" + bundle_path)
        # try:
        #     os.makedirs(bundle_path)
        # except OSError as e:
        #     if e.errno != errno.EEXIST:
        #         return False

        # Get the tar file
        tar_file = self._get_tar_from_bundle(bundle_path)
        if tar_file is None:
            ab = AsimovBundle()
            ab.get_latest_master_bundle(bundle_path)

        tar_file = self._get_tar_from_bundle(bundle_path)
        assert tar_file is not None, "Error tar file not found."

        # Read/cache file data
        with open(tar_file, 'rb') as f:
            file_data = f.read()
        file_size = len(file_data)

        # Get package info from file name
        tar_file = tar_file.split("/")[
            -1]  # Remove extraneous path info

        # Print current version (git sha) for context (in case of failure)
        udsc.connect()
        vers_dict = udsc.git_sha()
        logger.info("Current version: " + str(vers_dict))

        #################################################################
        # Start appropriate session and get required security access
        #################################################################
        # Start extended, then programming, diagnostic session
        udsc.diagnostic_session_control(uds.SessionID.EXTENDED)
        udsc.diagnostic_session_control(uds.SessionID.PROGRAMMING)

        # Get the required security level
        udsc.security_access(SecurityLevel.ECU_FLASHING)

        #################################################################
        # Check programming preconditions then request download
        #################################################################
        udsc.routine_control(
            uds.RoutineID.CHECK_PROGRAMMING_PRECONDITION,
            uds.RoutineControlType.START_ROUTINE)
        udsc.request_download(file_size)

        #################################################################
        # Start file transfer and fw update
        #################################################################
        logger.info(
            "File transfer: {} ({} Bytes)".format(tar_file, file_size))

        # Local variables to keep track of file transfer, since
        # we need to transfer the file in chunks
        pending_bytes = file_size
        sent_bytes = 0
        max_payload_size = udsc.uds_client.tx_payload_size

        # Transfer loop
        while sent_bytes < file_size:
            # Determine how many bytes we can send out next
            if pending_bytes > max_payload_size:
                tx_size = max_payload_size
            else:
                tx_size = pending_bytes

            # Prepare next transfer payload and complete transfer
            tx_payload = file_data[sent_bytes: sent_bytes + tx_size]
            assert udsc.transfer_data(tx_payload), (
                "Transfer data {}/{} bytes".format(sent_bytes,
                                                    file_size)
            )

            # Update our local transfer state
            sent_bytes += tx_size
            pending_bytes -= tx_size

        # Done! Request transfer exit
        logger.info("File transfer complete!")
        udsc.request_transfer_exit()

        # Check programming dependencies to 1) start firmware update and
        # 2) poll firmware update status until firmware update is complete
        # Note: takes a long time

        ret_dict = {"result": False}
        ret_dict["result"] = udsc.routine_control(
            uds.RoutineID.CHECK_PROGRAMMING_DEPENDENCIES,
            uds.RoutineControlType.START_ROUTINE)

        # Wait for update to complete, then check result
        # update_thread.join()
        assert ret_dict["result"]

        udsc.diagnostic_session_control(uds.SessionID.DEFAULT)

        with AsimovUDSClientManager(udsc.mcu,
                                    UDSClientTransportType.DoIP) as udsm:
            logger.info("Resetting.")
            assert udsm.reset()


    # def fetch_cal_file_test(self, s32v):
    #     s32v.connect()


    #     yield
    #     s32v.disconnect()

